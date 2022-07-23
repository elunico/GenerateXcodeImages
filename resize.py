import cv2
import argparse
import os.path
import os

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', default='app-icon.png', help='Path to the image')
    ap.add_argument('-c', '--clean', action='store_true', help='Clean the out directory before resizing')
    return ap.parse_args()


new_sizes = [
    # ((width, height), 'suffix')
    ((40, 40), '-20@2x'),
    ((60, 60), '-20@3x'),
    ((58, 58), '-29@2x'),
    ((87, 87), '-29@3x'),
    ((80, 80), '-40@2x'),
    ((120, 120), '-40@3x'),
    ((120, 120), '@2x'),
    ((180, 180), '@3x'),
    ((20, 20), '-20~ipad'),
    ((40, 40), '-20@2x~ipad'),
    ((29, 29), '-29~ipad'),
    ((58, 58), '-29@2x~ipad'),
    ((40, 40), '-40~ipad'),
    ((80, 80), '-40@2x~ipad'),
    ((76, 76), '~ipad'),
    ((152, 152), '@2x~ipad'),
    ((167, 167), '-83.5@2x~ipad'),
    ((1024, 1024), '~ios-marketing'),
    ((16, 16), '~mac'),
    ((32, 32), '-16@2x~mac'),
    ((32, 32), '-32~mac'),
    ((64, 64), '-32@2x~mac'),
    ((128, 128), '-128~mac'),
    ((256, 256), '-128@2x~mac'),
    ((256, 256), '-256~mac'),
    ((512, 512), '-256@2x~mac'),
    ((512, 512), '-512~mac'),
    ((1024, 1024), '-512@2x~mac'),
]


def main():
    arguments = parse_args()

    if not os.path.exists(arguments.image):
        raise ValueError('Source image does not exist')

    image = cv2.imread(arguments.image, cv2.IMREAD_UNCHANGED)

    if os.path.exists('out') and arguments.clean:
        answer = input('Remove out directory? (y/n) ')
        if answer.strip().lower() == 'y':
            print('Removing out directory')
            os.system('rm -rf out')
    elif os.path.exists('out') and not os.path.isdir('out'):
        raise Exception('out exists but is not a directory')

    if not os.path.isdir('out'):
        os.makedirs(os.path.join('out', 'mac'))
        os.makedirs(os.path.join('out', 'ios'))


    for i in new_sizes:
        size = i[0]
        name = f'{arguments.image.replace(".png", "")}{i[1]}.png'.replace('/', '_')
        resized = cv2.resize(image, size)
        if 'mac' in i[1]:
            print("Writing mac image '{}', ({}x{})".format(name, i[0][0], i[0][1]))
            cv2.imwrite(os.path.join('out', 'mac', name), resized)
        else:
            print("Writing ios image '{}', ({}x{})".format(name, i[0][0], i[0][1]))
            cv2.imwrite(os.path.join('out', 'ios', name), resized)

if __name__ == '__main__':
    main()
