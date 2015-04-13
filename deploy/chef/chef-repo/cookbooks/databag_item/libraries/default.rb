# Copyright (c) Microsoft Open Technologies (Shanghai) Co. Ltd.  All rights reserved.
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

require 'forwardable'
require 'json'

module MSOpentechCN
  module Chef

    # A Mash that could fallback to databag
    class MashWithFallBack < ::Mash
      extend Forwardable

      def_delegators(:@data, *(::Mash.instance_methods-[:object_id, :__send__, :[]]))

      def initialize(data, fallback_data)
        @data = data
        @fallback_data = fallback_data
      end

      def self.wrap(data, fallback_data)
        if data == nil then
          data = fallback_data
          fallback_data = nil

          return data if data == nil
        end

        return data unless data.is_a?(::Mash)
        return MashWithFallBack.new(data, fallback_data)
      end

      def [](key)
        return get_data_with_fallback(key, @data, @fallback_data)
      end

      private
      def get_data_with_fallback(key, data, fallback_data)
        result = data[key]
        fallback_result = fallback_data[key] if fallback_data != nil
        return MashWithFallBack.wrap(result, fallback_result)
      end
    end

    class DatabagItem
      def initialize(secret, environment, bag_id)
        raise 'Missing bag_id parameter' unless bag_id
        raise 'Missing environment' unless environment
        ::Chef::Log.info("Load databag '#{bag_id}' for environment #{environment}")

        begin
          if secret == nil
            data_bag = ::Chef::DataBagItem.load(environment, bag_id)
          else
            data_bag = ::Chef::EncryptedDataBagItem.load(environment, bag_id, secret)
          end

          @attributes = ::Chef::Node::Attribute.new(data_bag.to_hash, {}, {}, {})

        rescue Exception => e
          # Capture the exception so the chef script could continue executing.
          # 
          # Fall-back to use values in environment if the failed to load databag
          # This is for backward compatibility that some environment may not have databag available
          # 
          ::Chef::Log.warn "Failed to load databag for environment #{environment}. Because of '#{e}'. It may because the databag does not exist for the environment."
        end
      end

      def [](attrib)
        (@attributes == nil)? nil : @attributes[attrib]
      end
    end

    module ChefDSL
      include Chef::DataBagSecret

      @@initialized = false

      def initialize_chef_dsl
        return if @@initialized

        @@databag_items = Hash.new
        @@secret = load_databag_secret(node) 
        @@initialized = true
      end

      def databag_item(bag_id=nil)
        initialize_chef_dsl

        bag_id = (bag_id or 'default')
        unless @@databag_items.has_key? bag_id
          @@databag_items[bag_id] = DatabagItem.new(@@secret, node.chef_environment, bag_id)
        end

        @@databag_items[bag_id]
      end
    end
  end
end


# Patch our DSL extension into Chef
class Chef

  # Monkey patch the node[] method so we can access databag item from there
  # 
  class Node
    include MSOpentechCN::Chef::ChefDSL

    old_accesser = instance_method(:[])

    Chef::Log.info

    define_method(:[]) do |key|

      node_data = old_accesser.bind(self).(key)

      # Put all dependence cookbooks as blacklist to avoid indefinite recursive 
      # 
      if %w(databag_item citadel chef_solo).include?(key.to_s)
        return node_data
      end

      # directly return data if the databag_item cookbook is not loaded yet
      # This could happen during the chef environment loading phase
      # 
      if old_accesser.bind(self).('databag_item') == nil
        return node_data
      end

      # Now we are working ...
      # Make sure data from databag has higher priority then environment
      #
      return MSOpentechCN::Chef::MashWithFallBack.wrap(databag_item[key], node_data)
    end
  end

  # Make sure we can access to databagItem with databag_item[] interface from recipe
  # 
  class Recipe
    include MSOpentechCN::Chef::ChefDSL
  end

  # Make sure we can access to databagItem with databag_item[] interface from resource
  # 
  class Resource
    include MSOpentechCN::Chef::ChefDSL
  end

  # Make sure we can access to databagItem with databag_item[] interface from provider
  # 
  class Provider
    include MSOpentechCN::Chef::ChefDSL
  end

  # Make sure we can access to databagItem with databag_item[] interface from recipe
  # 
  module Mixin
    module Template
      module ChefContext
        include MSOpentechCN::Chef::ChefDSL
      end

      ::Erubis::Context.send(:include, ChefContext)
    end
  end

end
