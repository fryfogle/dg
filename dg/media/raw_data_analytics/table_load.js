window.onload = table_load;
window.dataReadyForDownload=0;

function excelCreate(keyset,formated_json){
    var dfd = $.Deferred();
    var customTitle='rawdata_';
    var d = new Date();
    customTitle= customTitle + d.getFullYear()+d.getMonth()+d.getDay()+'T'+d.getHours()+d.getMinutes();
    header_dict={'keys':[]};
    var cell_format = {
        bold: 0,
        font_size: 10,
        text_wrap: true
    };
    var data_json = {
        data: {
            sheet_heading: 'Raw Data Analytics',
            sheet_name: customTitle,
            data: formated_json
        }
    };

    for(var i=0;i<keyset.length;i++){
        var col = {
            'column_width': 8.45,
            'formula': null,
            'label': '',
            'total': false
        }
        col['label'] = keyset[i];
        header_dict['keys'].push(col);
    }
    var json_to_send = {
        header: header_dict,
        data: data_json,
        cell_format: cell_format
    }
    
    xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/loop/get_payment_sheet/", true);
    xhttp.onreadystatechange = function() {
        var a;
        if (xhttp.readyState === 4 && xhttp.status === 200) {
            a = document.createElement('a');
            console.log(xhttp.response);
            a.href = window.URL.createObjectURL(xhttp.response);
            a.download = customTitle;
            a.style.display = 'none';
            a.id='downloadLink';
            document.body.appendChild(a);
            return a;
            //return a.click();
        }
    };
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.responseType = 'blob';
    xhttp.send(JSON.stringify(json_to_send));
    dfd.resolve("finish");
    return dfd.promise();
}

function table_load()
{               
	
	var json = $("#tablex").data("val-json");
	
	var formated_json = [];
	var full_data = [];
	var keyset = Object.keys(json);
	var interkeys = Object.keys(json[keyset[0]]);
	for (var i=0; i<interkeys.length; i++){
		var obj=[];
		for (var j=0; j<keyset.length;j++){
			obj[j] = json[keyset[j]][interkeys[i]];
		}
		formated_json.push(obj);
	}
    excelCreate(keyset,formated_json).then(function(result){
        dataReadyForDownload=1;
    });
    console.log("out");
	full_data.push(formated_json);
	
	var column_arr = [];
	for(var i=0; i<keyset.length; i++)
	{
		var column_obj = {};
		column_obj["sTitle"] = keyset[i];
		column_obj["sClass"] = "a-center";
		column_arr.push(column_obj);

	}
	
	$('#example').dataTable( {
		"sDom":'T<"clear">lfrtip',
		"bAutoWidth":false,
        "aaData": formated_json,
        "aoColumns": column_arr,
        "oTableTools":{

            "sSwfPath": "/media/social_website/scripts/libs/tabletools_media/swf/copy_csv_xls.swf",
			"aButtons": [
	                           {
	                               "sExtends": "copy",
	                               "sButtonText": "Copy to Clipboard"
	                           },
	                           {
	                               "sExtends": "text",
	                               "sButtonText": "Download in Excel",
	                               "fnClick": function(nButton, oConfig) {

	                               	    /*while(!dataReadyForDownload){
                                            $("#downloadingDiv").show();
                                        }*/
                                        $('#downloadLink')[0].click();
                                        /*$('#downloadLink').click(function(e){
                                            console.log('dkjfks');
                                            e.preventDefault();
                                            location.href = ($('#downloadLink').attr("href"));
                                        });*/
                                        
                					}
	                           }
	                       ]
                    }
    } );

}