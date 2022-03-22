def file_type(filename):
    result = ""
    arr = filename.split('.')
    result = arr[1]
    return result

def serve_static_file(route):
    filename = ""
    path = ""
    filetype = ""
    arr = route[1:].split('/')
    if arr[0] == "":
        filename = "index.html"
        path = f"static/{filename}"
        filetype = "html"
    elif arr[0]=="images" and len(arr) == 2 :
        filename = arr[1]
        filetype = file_type(filename)
        path = f"static/images/{filename}"
    elif len(arr) == 1:
        filename = arr[0]
        path = f"static/{filename}"
        filetype = file_type(filename)
    
    return filename , path , filetype
