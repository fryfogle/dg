// This is the home/status view shown at root url. It contains the welcome message, usage instructions and some offline db stats.
// It checks whether offline db exists or not, if not initiates the full download module.

define([
    'jquery',
    'underscore',
    'layoutmanager',
    'indexeddb_backbone_config',
    'views/full_download',
    'configs',
    'collections/upload_collection',
    'views/notification',
    'models/user_model',
    'offline_utils',
    'indexeddb-backbone'
], function(jquery, underscore, layoutmanager, indexeddb, FullDownloadView, configs, upload_collection, notifs_view, User, Offline) {

    var StatusView = Backbone.Layout.extend({
        template: "#status",
        timestamp: null,
        upload_entries: null,
        events: {
            "click button#download": "download",
            "click button#reset_database": "reset"
        },

        initialize: function() {
            _(this).bindAll('fill_status');
            this.fill_status();
        },

        serialize: function() {
            // send the following to the template
            var language = User.get('language');
            return {
                language: language,
                configs: configs,
                full_d_timestamp: this.full_download_timestamp,
                inc_d_timestamp: this.inc_download_timestamp,
                num_upload_entries: this.upload_entries,
                db_version: this.db_version,
                upload_collection: upload_collection.toJSON()
            }
        },

        // fills the stats on the view
        fill_status: function() {
            var that = this;
            // # of unsynced entries
            that.upload_entries = upload_collection.length;
            // current version of IndexedDB - its wrong - shd take the last migration instead of first
            that.db_version = indexeddb.migrations[0].version;

            // fetch last full download's timestamp
            Offline.fetch_object("meta_data", "key", "last_full_download")
                .done(function(model) {
                    that.full_download_timestamp = new Date(model.get('timestamp'));
                    // fetch last inc download's timestamp
                    Offline.fetch_object("meta_data", "key", "last_inc_download")
                        .done(function(model) {
                            that.inc_download_timestamp = new Date(model.get('timestamp'));
                            // all stats fetched....render the view
                            that.render();
                        })
                        .fail(function(model, error) {
                            // all stats fetched....render the view
                            that.inc_download_timestamp = "Never";
                            that.render();
                        });
                    that.render();
                })
                .fail(function(model, error) {
                    console.log("STATUS: error while fetching last_downloaded from meta_data objectStore");
                    console.log(error);
                    if (error == "Not Found") {
                        // offline db not populated...full donwload never finished
                        that.full_download_timestamp = "Never";
                        that.render()
                            .done(function() {
                                //Start full download automatically
                                that.download();
                            });
                    }
                });


        },

        //method to initiate full download
        download: function() {
            var dfd = new $.Deferred();
            //create full download view
            if (!this.full_download_v) {
                this.full_download_v = new FullDownloadView();
            }
            // set full download as subview
            this.setView("#modal", this.full_download_v).render();
            var that = this;
            //start full download
            this.full_download_v.start_full_download()
                .done(function() {
                    // render status view once full download finishes
                    that.fill_status();
                    notifs_view.add_alert({
                        notif_type: "success",
                        message: "Successfully downloaded the database"
                    });
                    dfd.resolve();
                })
                .fail(function(error) {
                    notifs_view.add_alert({
                        notif_type: "error",
                        message: "Failed to download the database : " + error
                    });
                    dfd.reject();
                });
            return dfd;
        },

        // Resets the offline db
        reset: function() {
            // check if user has unsynced data in upload queue
            if(upload_collection.length > 0){
                var val = confirm("You will lose unsynced data. Click 'Ok' to proceed and 'Cancel' to abort")
                if (val == true) {
                    Offline.reset_database();
                }    
            }
            else {
                var val = confirm("Your database will be deleted and downloaded again. Are you sure you want to continue?")
                if (val == true) {
                    Offline.reset_database();
                }
            }
        }
    });

    // Our module now returns our view
    return StatusView;
});
