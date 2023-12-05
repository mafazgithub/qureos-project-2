from flask import Flask, request, send_file
from flask_restful import Resource, Api
from flask_uploads import UploadSet, configure_uploads, IMAGES, DOCUMENTS
from flask_restful_swagger_3 import Api as SwaggerApi, Resource as SwaggerResource

app = Flask(__name__)
api = Api(app)
swagger = SwaggerApi(app)

# Configure file uploads
files = UploadSet("files", IMAGES + DOCUMENTS)
app.config["UPLOADED_FILES_DEST"] = "uploads"
configure_uploads(app, files)


class FileResource(SwaggerResource):
    @swagger.doc({
        "tags": ["File Management"],
        "description": "Download a file",
        "parameters": [
            {"name": "filename", "in": "path", "required": True, "description": "Name of the file"},
        ],
        "responses": {"200": {"description": "File downloaded successfully"}},
    })
    def get(self, filename):
        try:
            return send_file(f"uploads/{filename}")
        except Exception as e:
            return {"error": str(e)}, 404

    @swagger.doc({
        "tags": ["File Management"],
        "description": "Delete a file",
        "parameters": [
            {"name": "filename", "in": "path", "required": True, "description": "Name of the file"},
        ],
        "responses": {"200": {"description": "File deleted successfully"}},
    })
    def delete(self, filename):
        try:
            # Add logic for deleting the file from storage
            return {"message": f"{filename} deleted successfully"}
        except Exception as e:
            return {"error": str(e)}, 500


class FileListResource(SwaggerResource):
    @swagger.doc({
        "tags": ["File Management"],
        "description": "List all available files",
        "responses": {"200": {"description": "List of available files"}},
    })
    def get(self):
        # Add logic for listing available files
        files_list = []  # Replace with actual list of files
        return {"files": files_list}

    @swagger.doc({
        "tags": ["File Management"],
        "description": "Upload a file",
        "parameters": [
            {"name": "file", "in": "formData", "required": True, "type": "file", "description": "File to upload"},
        ],
        "responses": {"200": {"description": "File uploaded successfully"}},
    })
    def post(self):
        try:
            file = request.files["file"]
            if file:
                filename = files.save(file)
                # Add logic for storing file details in the database
                return {"message": f"{filename} uploaded successfully"}
        except Exception as e:
            return {"error": str(e)}, 500


class FileShareResource(SwaggerResource):
    @swagger.doc({
        "tags": ["File Management"],
        "description": "Share a file",
        "parameters": [
            {"name": "filename", "in": "path", "required": True, "description": "Name of the file"},
        ],
        "responses": {"200": {"description": "File shared successfully"}},
    })
    def post(self, filename):
        # Add logic for sharing the file
        # This might involve generating a unique link or managing access permissions
        return {"message": f"{filename} shared successfully"}


# API routes
api.add_resource(FileResource, "/file/<string:filename>")
api.add_resource(FileListResource, "/files")
api.add_resource(FileShareResource, "/file/share/<string:filename>")

if __name__ == "__main__":
    app.run(debug=True)
