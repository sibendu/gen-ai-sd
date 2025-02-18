from sketchify import sketch

img = "image/m.jpg"
output = "image/m3"

print(f'Starting to proces')

sketch.normalsketch(img, './', output, scale=10)

print(f'Completed processing')