__doc__ = "provides modules to load and save images and tiff-image sequencec"

import numpy as np
from scipy import ndimage

from PIL import Image


def save(_file, data):
    """
    save image to disk
    
    Parameters
    ---------
    
    _file: path where to save file
    
    data: numpy array containing the image data
     
    """
    
    Image.fromarray(data).save(_file)
    return None
    
    

def load(_file, zoom=None, correction=False):
    """
    loads an image using PIL and substracts 2**15 for 16-bit images 
    
    Parameters
    ----------
    
    _file: location of images 
    
    zoom: reduces m x n image to m/zoom x n/zoom
    
    correction: if True corrects for the 2**15 offset in some 16-bit Tif images
    
    Returns
    -------
    
    data: numpy array containing the data, data type according to input image
    
    """

    try:
        tif = Image.open(_file)
    except:
        if ".tiff" in _file:
            tif = Image.open(_file.replace(".tiff", ".tif"))
        else:
            tif = Image.open(_file.replace(".tif", ".tiff"))

    tiffcorrection = 0
    if tif.mode == "F":
        precision = np.float32
    elif tif.mode == "F;32BF": # files saved with ImageJ
        tif.mode = "F"
        precision = np.float32
    elif tif.mode == "I;16":
        precision = np.uint16
        if correction:
            tiffcorrection = 2 ** 15 # 16bit images saved with LabView
    elif tif.mode == "I;16B":
        precision = np.uint16
    elif tif.mode in ['L', 'P']:
        precision = np.uint8

    data = np.array(tif.getdata(), dtype=precision).reshape(tif.size[::-1])
    
    if zoom is not None:
        data = ndimage.interpolation.zoom(data, 1.0 / zoom, mode="nearest")

    return data - tiffcorrection
    


def loadtiffstack(_file, Zoom=None, correction=False):
    """
    Load images from a tiff-stack and returns them as a s x mxn numpy array
    
    Parameters
    ----------
    
    _file: location of images 
    
    zoom: reduces m x n image to m/zoom x n/zoom (not implemented yet)
    
    correction: if True corrects for the 2**15 offset in some 16-bit Tif images
    
    
    Returns
    --------
    
    data: numpy array containing the data, data type according to input image
    dimensions are (frames,heigth,width)
    
        """
    try:
        tif = Image.open(_file)
    except:
        if ".tiff" in _file:
            tif = Image.open(_file.replace(".tiff", ".tif"))
        else:
            tif = Image.open(_file.replace(".tif", ".tiff"))
            
   
    if tif.mode == "F":
        precision = np.float32
    elif tif.mode == "F;32BF": # files saved with ImageJ
        tif.mode = "F"
        precision = np.float32
    elif tif.mode == "I;16":
        precision = np.uint16
    elif tif.mode == "I;16B":
        precision = np.uint16
    elif tif.mode in ['L', 'P']:
        precision = np.uint8

   
    
    while(True):
        try:
            if tif.mode == "F;32BF":
                tif.mode = "F"
            yield np.array(tif.getdata(), dtype=precision).reshape(tif.size[::-1])
            tif.seek(tif.tell() + 1)
        except EOFError:
            break

class MultiImageSequence:
    """
    Class for handling multiple large TIF stacks of same size without 
    the need to load them completely to memory, creates an iterable object wich 
    yields a list of images of each stack
    
    Parameters
    ----------
    
    imlist: list of paths to tiffstacks or list of image instances (PIL.Image)    
       
    """
    
    def __init__(self, imlist):
        """
        the paths to the images are stored in a list, eg.
        [TFP_par, TFP_perp, YFP_par, YFP_perp, ...]
        """
        
        self.stacklist = []
        
        # if imlist contains paths to images open the images
        if isinstance(imlist[0], str):
            
            for _path in imlist:
                try:
                    
                    self.stacklist.append(Image.open(_path))
                    
                except:
                    IOError
                    self.stacklist.append(None)

        # if the list already contains images
        else:       
            self.stacklist = imlist
                              

        self.imsize = self.stacklist[0].size[::-1]
        
    def __getitem__(self, ix):
        """
        returns the images of each stack of index "ix"
        """
        
        outlist = []
        for _image in self.stacklist:

            try:
                if ix:
                    _image.seek(ix)
        
                outlist.append(getimdata(_image))
        
            except EOFError:
                raise IndexError # end of sequence
        return outlist
            
            
    def imsize(self):
        """
        return size of the individual images in the stack
        """
        return self.imsize
       
def getimdata(im_instance):
    """
    get numpy array from PIL image instance
    
    Parameters
    ----------
    im_instance: PIL image
    
    Returns
    -------
    np_image: image as numpy array    
    """
    im_instance.mode = "F"
    return np.array(im_instance.getdata(), 
             dtype=np.float32).reshape(im_instance.size[::-1])