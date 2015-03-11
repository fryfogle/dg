var Resumable=function(e){function o(e,t){var r=this;r.opts={},r.getOpt=e.getOpt,r._prevProgress=0,r.resumableObj=e,r.file=t,r.fileName=t.fileName||t.name,r.size=t.size,r.relativePath=t.webkitRelativePath||r.fileName,r.uniqueIdentifier=n.generateUniqueIdentifier(t);var i=!1,s=function(e,t){switch(e){case"progress":r.resumableObj.fire("fileProgress",r);break;case"error":r.abort(),i=!0,r.chunks=[],r.resumableObj.fire("fileError",r,t);break;case"success":if(i)return;r.resumableObj.fire("fileProgress",r),r.isComplete()&&r.resumableObj.fire("fileSuccess",r,t);break;case"retry":r.resumableObj.fire("fileRetry",r)}};return r.chunks=[],r.abort=function(){n.each(r.chunks,function(e){e.status()=="uploading"&&e.abort()}),r.resumableObj.fire("fileProgress",r)},r.cancel=function(){var e=r.chunks;r.chunks=[],n.each(e,function(e){e.status()=="uploading"&&(e.abort(),r.resumableObj.uploadNextChunk())}),r.resumableObj.removeFile(r),r.resumableObj.fire("fileProgress",r)},r.retry=function(){r.bootstrap(),r.resumableObj.upload()},r.bootstrap=function(){r.abort(),i=!1,r.chunks=[],r._prevProgress=0;var e=r.getOpt("forceChunkSize")?Math.ceil:Math.floor;for(var t=0;t<Math.max(e(r.file.size/r.getOpt("chunkSize")),1);t++)r.chunks.push(new u(r.resumableObj,r,t,s))},r.progress=function(){if(i)return 1;var e=0,t=!1;return n.each(r.chunks,function(n){n.status()=="error"&&(t=!0),e+=n.progress(!0)}),e=t?1:e>.999?1:e,e=Math.max(r._prevProgress,e),r._prevProgress=e,e},r.isUploading=function(){var e=!1;return n.each(r.chunks,function(t){if(t.status()=="uploading")return e=!0,!1}),e},r.isComplete=function(){var e=!1;return n.each(r.chunks,function(t){var n=t.status();if(n=="pending"||n=="uploading"||t.preprocessState===1)return e=!0,!1}),!e},r.bootstrap(),this}function u(e,t,r,i){var s=this;s.opts={},s.getOpt=e.getOpt,s.resumableObj=e,s.fileObj=t,s.fileObjSize=t.size,s.offset=r,s.callback=i,s.lastProgressCallback=new Date,s.tested=!1,s.retries=0,s.pendingRetry=!1,s.preprocessState=0;var o=s.getOpt("chunkSize");return s.loaded=0,s.startByte=s.offset*o,s.endByte=Math.min(s.fileObjSize,(s.offset+1)*o),s.fileObjSize-s.endByte<o&&!s.getOpt("forceChunkSize")&&(s.endByte=s.fileObjSize),s.xhr=null,s.test=function(){s.xhr=new XMLHttpRequest;var e=function(e){s.tested=!0;var t=s.status();t=="success"?(s.callback(t,s.message()),s.resumableObj.uploadNextChunk()):s.send()};s.xhr.addEventListener("load",e,!1),s.xhr.addEventListener("error",e,!1);var t=[],r=s.getOpt("query");typeof r=="function"&&(r=r(s.fileObj,s)),n.each(r,function(e,n){t.push([encodeURIComponent(e),encodeURIComponent(n)].join("="))}),t.push(["resumableChunkNumber",encodeURIComponent(s.offset+1)].join("=")),t.push(["resumableChunkSize",encodeURIComponent(s.getOpt("chunkSize"))].join("=")),t.push(["resumableCurrentChunkSize",encodeURIComponent(s.endByte-s.startByte)].join("=")),t.push(["resumableTotalSize",encodeURIComponent(s.fileObjSize)].join("=")),t.push(["resumableIdentifier",encodeURIComponent(s.fileObj.uniqueIdentifier)].join("=")),t.push(["resumableFilename",encodeURIComponent(s.fileObj.fileName)].join("=")),t.push(["resumableRelativePath",encodeURIComponent(s.fileObj.relativePath)].join("=")),s.xhr.open("GET",n.getTarget(t)),s.xhr.withCredentials=s.getOpt("withCredentials"),n.each(s.getOpt("headers"),function(e,t){s.xhr.setRequestHeader(e,t)}),s.xhr.send(null)},s.preprocessFinished=function(){s.preprocessState=2,s.send()},s.send=function(){var e=s.getOpt("preprocess");if(typeof e=="function")switch(s.preprocessState){case 0:e(s),s.preprocessState=1;return;case 1:return;case 2:}if(s.getOpt("testChunks")&&!s.tested){s.test();return}s.xhr=new XMLHttpRequest,s.xhr.upload.addEventListener("progress",function(e){new Date-s.lastProgressCallback>s.getOpt("throttleProgressCallbacks")*1e3&&(s.callback("progress"),s.lastProgressCallback=new Date),s.loaded=e.loaded||0},!1),s.loaded=0,s.pendingRetry=!1,s.callback("progress");var t=function(e){var t=s.status();if(t=="success"||t=="error")s.callback(t,s.message()),s.resumableObj.uploadNextChunk();else{s.callback("retry",s.message()),s.abort(),s.retries++;var n=s.getOpt("chunkRetryInterval");n!==undefined?(s.pendingRetry=!0,setTimeout(s.send,n)):s.send()}};s.xhr.addEventListener("load",t,!1),s.xhr.addEventListener("error",t,!1);var r={resumableChunkNumber:s.offset+1,resumableChunkSize:s.getOpt("chunkSize"),resumableCurrentChunkSize:s.endByte-s.startByte,resumableTotalSize:s.fileObjSize,resumableIdentifier:s.fileObj.uniqueIdentifier,resumableFilename:s.fileObj.fileName,resumableRelativePath:s.fileObj.relativePath,resumableTotalChunks:s.fileObj.chunks.length},i=s.getOpt("query");typeof i=="function"&&(i=i(s.fileObj,s)),n.each(i,function(e,t){r[e]=t});var o=s.fileObj.file.slice?"slice":s.fileObj.file.mozSlice?"mozSlice":s.fileObj.file.webkitSlice?"webkitSlice":"slice",u=s.fileObj.file[o](s.startByte,s.endByte),a=null,f=s.getOpt("target");if(s.getOpt("method")==="octet"){a=u;var l=[];n.each(r,function(e,t){l.push([encodeURIComponent(e),encodeURIComponent(t)].join("="))}),f=n.getTarget(l)}else a=new FormData,n.each(r,function(e,t){a.append(e,t)}),a.append(s.getOpt("fileParameterName"),u);s.xhr.open("POST",f),s.xhr.withCredentials=s.getOpt("withCredentials"),n.each(s.getOpt("headers"),function(e,t){s.xhr.setRequestHeader(e,t)}),s.xhr.send(a)},s.abort=function(){s.xhr&&s.xhr.abort(),s.xhr=null},s.status=function(){return s.pendingRetry?"uploading":s.xhr?s.xhr.readyState<4?"uploading":s.xhr.status==200?"success":n.contains(s.getOpt("permanentErrors"),s.xhr.status)||s.retries>=s.getOpt("maxChunkRetries")?"error":(s.abort(),"pending"):"pending"},s.message=function(){return s.xhr?s.xhr.responseText:""},s.progress=function(e){typeof e=="undefined"&&(e=!1);var t=e?(s.endByte-s.startByte)/s.fileObjSize:1;if(s.pendingRetry)return 0;var n=s.status();switch(n){case"success":case"error":return 1*t;case"pending":return 0*t;default:return s.loaded/(s.endByte-s.startByte)*t}},this}if(this instanceof Resumable){this.version=1,this.support=typeof File!="undefined"&&typeof Blob!="undefined"&&typeof FileList!="undefined"&&(!!Blob.prototype.webkitSlice||!!Blob.prototype.mozSlice||!!Blob.prototype.slice||!1);if(!this.support)return!1;var t=this;t.files=[],t.defaults={chunkSize:1048576,forceChunkSize:!1,simultaneousUploads:3,fileParameterName:"file",throttleProgressCallbacks:.5,query:{},headers:{},preprocess:null,method:"multipart",prioritizeFirstAndLastChunk:!1,target:"/",testChunks:!0,generateUniqueIdentifier:null,maxChunkRetries:undefined,chunkRetryInterval:undefined,permanentErrors:[404,415,500,501],maxFiles:undefined,withCredentials:!1,maxFilesErrorCallback:function(e,n){var r=t.getOpt("maxFiles");alert("Please upload "+r+" file"+(r===1?"":"s")+" at a time.")},minFileSize:1,minFileSizeErrorCallback:function(e,r){alert(e.fileName||e.name+" is too small, please upload files larger than "+n.formatSize(t.getOpt("minFileSize"))+".")},maxFileSize:undefined,maxFileSizeErrorCallback:function(e,r){alert(e.fileName||e.name+" is too large, please upload files less than "+n.formatSize(t.getOpt("maxFileSize"))+".")},fileType:[],fileTypeErrorCallback:function(e,n){alert(e.fileName||e.name+" has type not allowed, please upload files of type "+t.getOpt("fileType")+".")}},t.opts=e||{},t.getOpt=function(e){var t=this;if(e instanceof Array){var r={};return n.each(e,function(e){r[e]=t.getOpt(e)}),r}if(t instanceof u){if(typeof t.opts[e]!="undefined")return t.opts[e];t=t.fileObj}if(t instanceof o){if(typeof t.opts[e]!="undefined")return t.opts[e];t=t.resumableObj}if(t instanceof Resumable)return typeof t.opts[e]!="undefined"?t.opts[e]:t.defaults[e]},t.events=[],t.on=function(e,n){t.events.push(e.toLowerCase(),n)},t.fire=function(){var e=[];for(var n=0;n<arguments.length;n++)e.push(arguments[n]);var r=e[0].toLowerCase();for(var n=0;n<=t.events.length;n+=2)t.events[n]==r&&t.events[n+1].apply(t,e.slice(1)),t.events[n]=="catchall"&&t.events[n+1].apply(null,e);r=="fileerror"&&t.fire("error",e[2],e[1]),r=="fileprogress"&&t.fire("progress")};var n={stopEvent:function(e){e.stopPropagation(),e.preventDefault()},each:function(e,t){if(typeof e.length!="undefined"){for(var n=0;n<e.length;n++)if(t(e[n])===!1)return}else for(n in e)if(t(n,e[n])===!1)return},generateUniqueIdentifier:function(e){var n=t.getOpt("generateUniqueIdentifier");if(typeof n=="function")return n(e);var r=e.webkitRelativePath||e.fileName||e.name,i=e.size;return i+"-"+r.replace(/[^0-9a-zA-Z_-]/img,"")},contains:function(e,t){var r=!1;return n.each(e,function(e){return e==t?(r=!0,!1):!0}),r},formatSize:function(e){return e<1024?e+" bytes":e<1048576?(e/1024).toFixed(0)+" KB":e<1073741824?(e/1024/1024).toFixed(1)+" MB":(e/1024/1024/1024).toFixed(1)+" GB"},getTarget:function(e){var n=t.getOpt("target");return n.indexOf("?")<0?n+="?":n+="&",n+e.join("&")}},r=function(e){n.stopEvent(e),s(e.dataTransfer.files,e)},i=function(e){e.preventDefault()},s=function(e,r){var i=0,s=t.getOpt(["maxFiles","minFileSize","maxFileSize","maxFilesErrorCallback","minFileSizeErrorCallback","maxFileSizeErrorCallback","fileType","fileTypeErrorCallback"]);if(typeof s.maxFiles!="undefined"&&s.maxFiles<e.length+t.files.length){if(s.maxFiles!==1||t.files.length!==1||e.length!==1)return s.maxFilesErrorCallback(e,i++),!1;t.removeFile(t.files[0])}var u=[];n.each(e,function(e){if(s.fileType.length>0&&!n.contains(s.fileType,e.type.split("/")[1]))return s.fileTypeErrorCallback(e,i++),!1;if(typeof s.minFileSize!="undefined"&&e.size<s.minFileSize)return s.minFileSizeErrorCallback(e,i++),!1;if(typeof s.maxFileSize!="undefined"&&e.size>s.maxFileSize)return s.maxFileSizeErrorCallback(e,i++),!1;if(!t.getFromUniqueIdentifier(n.generateUniqueIdentifier(e))){var a=new o(t,e);t.files.push(a),u.push(a),t.fire("fileAdded",a,r)}}),t.fire("filesAdded",u)};return t.uploadNextChunk=function(){var e=!1;if(t.getOpt("prioritizeFirstAndLastChunk")){n.each(t.files,function(t){if(t.chunks.length&&t.chunks[0].status()=="pending"&&t.chunks[0].preprocessState===0)return t.chunks[0].send(),e=!0,!1;if(t.chunks.length>1&&t.chunks[t.chunks.length-1].status()=="pending"&&t.chunks[0].preprocessState===0)return t.chunks[t.chunks.length-1].send(),e=!0,!1});if(e)return!0}n.each(t.files,function(t){n.each(t.chunks,function(t){if(t.status()=="pending"&&t.preprocessState===0)return t.send(),e=!0,!1});if(e)return!1});if(e)return!0;var r=!1;return n.each(t.files,function(e){if(!e.isComplete())return r=!0,!1}),r||t.fire("complete"),!1},t.assignBrowse=function(e,r){typeof e.length=="undefined"&&(e=[e]),n.each(e,function(e){var n;e.tagName==="INPUT"&&e.type==="file"?n=e:(n=document.createElement("input"),n.setAttribute("type","file"),e.style.display="inline-block",e.style.position="relative",n.style.position="absolute",n.style.top=n.style.left=n.style.bottom=n.style.right=0,n.style.opacity=0,n.style.cursor="pointer",e.appendChild(n));var i=t.getOpt("maxFiles");typeof i=="undefined"||i!=1?n.setAttribute("multiple","multiple"):n.removeAttribute("multiple"),r?n.setAttribute("webkitdirectory","webkitdirectory"):n.removeAttribute("webkitdirectory"),n.addEventListener("change",function(e){s(e.target.files),e.target.value=""},!1)})},t.assignDrop=function(e){typeof e.length=="undefined"&&(e=[e]),n.each(e,function(e){e.addEventListener("dragover",i,!1),e.addEventListener("drop",r,!1)})},t.unAssignDrop=function(e){typeof e.length=="undefined"&&(e=[e]),n.each(e,function(e){e.removeEventListener("dragover",i),e.removeEventListener("drop",r)})},t.isUploading=function(){var e=!1;return n.each(t.files,function(t){if(t.isUploading())return e=!0,!1}),e},t.upload=function(){if(t.isUploading())return;t.fire("uploadStart");for(var e=1;e<=t.getOpt("simultaneousUploads");e++)t.uploadNextChunk()},t.pause=function(){n.each(t.files,function(e){e.abort()}),t.fire("pause")},t.cancel=function(){for(var e=t.files.length-1;e>=0;e--)t.files[e].cancel();t.fire("cancel")},t.progress=function(){var e=0,r=0;return n.each(t.files,function(t){e+=t.progress()*t.size,r+=t.size}),r>0?e/r:0},t.addFile=function(e){s([e])},t.removeFile=function(e){for(var n=t.files.length-1;n>=0;n--)t.files[n]===e&&t.files.splice(n,1)},t.getFromUniqueIdentifier=function(e){var r=!1;return n.each(t.files,function(t){t.uniqueIdentifier==e&&(r=t)}),r},t.getSize=function(){var e=0;return n.each(t.files,function(t){e+=t.size}),e},this}return new Resumable(e)};typeof module!="undefined"&&(module.exports=Resumable);