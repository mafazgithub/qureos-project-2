from flask import Flask, request, send_file
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
api = Api(app)

# Set the upload folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


class FileResource(Resource):
    def get(self, filename):
        try:
            return send_file(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        except Exception as e:
            return {"error": str(e)}, 404

    def delete(self, filename):
        try:
            # Add logic for deleting the file from storage
            os.remove(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return {"message": f"{filename} deleted successfully"}
        except Exception as e:
            return {"error": str(e)}, 500


class FileListResource(Resource):
    def get(self):
        # Add logic for listing available files
        files_list = []  # Replace with actual list of files
        return {"files": files_list}

    def post(self):
        try:
            file = request.files["file"]
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                # Add logic for storing file details in the database
                return {"message": f"{filename} uploaded successfully"}
        except Exception as e:
            return {"error": str(e)}, 500


class FileShareResource(Resource):
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
