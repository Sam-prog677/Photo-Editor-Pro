'''A file with the most of functions to the Cut Photos part.'''

#import moudles
import PIL
from PIL import Image

__author__ = "Sam Zhang"

def fill_image(image):
    '''To paste the old image onto the new image'''
    width, height = image.size
    #选取长和宽中较大值作为新图片的长
    #Choose the bigger number and make it the new photo's length
    new_image_length = width if width > height else height
    #生成新图片[白底]
    #Make a new photo[with white]
    new_image = PIL.Image.new(image.mode, (new_image_length, new_image_length), color='white')   #注意这个函数！
    #将之前的图粘贴在新图上，居中
    #Paste the photo before in the middle
    if width > height:
        #原图宽大于高，则填充图片的竖直维度  
        #If the old image's width is bigger than its height, then fill the image's vertical dimension
        #(x,y)二元组表示粘贴上图相对下图的起始位置,是个坐标点
        #Tuple (x,y) means the start point of pasting the upper images to the lower image, it's a coordinate
        new_image.paste(image, (0, int((new_image_length - height) / 2)))
    else:
        new_image.paste(image, (int((new_image_length - width) / 2),0))
    return new_image

def cut_image(image):
    '''To cut the new image to our final image'''
    width, height = image.size
    #因为朋友圈一行放3张图
    #Because of the wechat-moment can only put 3 images in a row, so we divid it in 3 pieces
    item_width = int(width / 3)
    box_list = []
    # (left, upper, right, lower)
    for i in range(0,3):
        for j in range(0,3):
            #print((i*item_width,j*item_width,(i+1)*item_width,(j+1)*item_width))
            box = (j*item_width,i*item_width,(j+1)*item_width,(i+1)*item_width)
            box_list.append(box)
    image_list = [image.crop(box) for box in box_list]
    return image_list

#保存
#Save
def save_images(image_list,image_name):
    '''Saves the new image to the computer'''
    index = 1
    for image in image_list:
        image.save("./output/output"+str(index)+'.png','PNG')
        image.save(str(image_name)+str(index) + '.png', 'PNG')
        index += 1