curl -XPUT 'localhost:9200/file-index/' -d '
{
   "mappings" : {
      "_default_" : {
         "_source" : {
            "enabled" : true
         },
         "_all" : {
            "analyzer" : "default",
            "enabled" : true
         },
         "properties" : {
            "file" : {
               "dynamic" : false,
               "properties" : {
                  "machine" : {
                     "type" : "multi_field",
                     "fields" : {
                        "machine" : {"type" : "string", "index" : "analyzed"},
                        "untouched" : {"type" : "string", "index" : "not_analyzed"}
                     }
                  },
                  "path" : {
                     "type" : "multi_field",
                     "fields" : {
                        "path" : {"type" : "string", "index" : "analyzed"},
                        "untouched" : {"type" : "string", "index" : "not_analyzed"}
                     }
                  },
                  "name" : {
                     "type" : "multi_field",
                     "fields" : {
                        "name" : {"type" : "string", "index" : "analyzed"},
                        "untouched" : {"type" : "string", "index" : "not_analyzed"}
                     }
                  },
                  "size" : {
                     "type" : "multi_field",
                     "fields" : {
                        "size" : {"type" : "string", "index" : "analyzed"},
                        "untouched" : {"type" : "string", "index" : "not_analyzed"}
                     }
                  },
                  "mtime" : {
                     "type" : "multi_field",
                     "fields" : {
                        "mtime" : {"type" : "string", "index" : "analyzed"},
                        "untouched" : {"type" : "string", "index" : "not_analyzed"}
                     }
                  },
                  "full" : {
                     "type" : "multi_field",
                     "fields" : {
                        "full" : {"type" : "string", "index" : "analyzed"},
                        "untouched" : {"type" : "string", "index" : "not_analyzed"}
                     }
                  }
               }
            }
         }
      }
   }
}
'