# Spot Image Stream

## Image types:
['PIXEL_FORMAT_UNKNOWN', 'PIXEL_FORMAT_GREYSCALE_U8', 'PIXEL_FORMAT_RGB_U8', 'PIXEL_FORMAT_RGBA_U8', 'PIXEL_FORMAT_DEPTH_U16', 'PIXEL_FORMAT_GREYSCALE_U16']

## Image Sources
image_sources = image_client.list_image_sources()
print(image_sources)
    # , name: "hand_color_image"
    # , name: "hand_color_in_hand_depth_frame"
    # , name: "hand_depth"
    # , name: "hand_depth_in_hand_color_frame"
    # , name: "hand_image"
