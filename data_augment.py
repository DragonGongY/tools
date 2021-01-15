
def crop(image, bbox, x, y, length)
    x, y, bbox = x.astype(np.int), y.astype(np.int), bbox.astype(np.int)
    x_min, y_min, x_max, y_max = bbox
    w,h =x_max-x_min, y_max-y_min

    image = image[y_min:y_min+h, x_min:x_min+w,:]
    x -=x_min
    y -=y_min
    bbox=np.array([0, 0, x_max-x_min, y_max-y_min])
    side_length=max(w,h)
    f_xy=float(length)/float(side_length)
    image, bbox, x, y =Transformer.scale(image, bbox, x, y, f_xy)
    
    new_w, new_h = image.shape[1], image.shape[0]
    
    

