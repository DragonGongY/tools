1、使用时只需要运行json_to_dataset.py即可。
２、标注完成以后，图像和json标签要放到同一个文件夹下。
３、需要设置不同物体的标签颜色时，需要更改label.py中cmap变量即可。
４、会在out_dir下自动生产Annotations和JPEGImages文件夹，Annotaions保存标签png图片,JPEGImages保存原始png图片。
５、在out_dir下会生产每张图片的标注展示图和label_names.txt