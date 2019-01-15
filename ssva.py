import argparse
from PIL import Image, ImageDraw
from math import floor

# Pixel numbers
number_width  = 5
number_height = 7
numbers = [Image.new("RGBA", (number_width, number_height)) for x in range(10)]
ImageDraw.Draw(numbers[0]).point(
	[
		(1, 1),
		(2, 1),
		(3, 1),
		(3, 2),
		(3, 3),
		(3, 4),
		(3, 5),
		(2, 5),
		(1, 5),
		(1, 4),
		(1, 3),
		(1, 2)
	], 
	(0, 0, 0, 255)
)
ImageDraw.Draw(numbers[1]).point(
	[
		(3, 1),
		(3, 2),
		(3, 3),
		(3, 4),
		(3, 5)
	], 
	(0, 0, 0, 255)
)
ImageDraw.Draw(numbers[2]).point(
	[
		(1, 1),
		(2, 1),
		(3, 1),
		(3, 2),
		(3, 3),
		(2, 3),
		(1, 3),
		(1, 4),
		(1, 5),
		(2, 5),
		(3, 5)
	], 
	(0, 0, 0, 255)
)
ImageDraw.Draw(numbers[3]).point(
	[
		(1, 1),
		(2, 1),
		(3, 1),
		(3, 2),
		(3, 3),
		(2, 3),
		(1, 3),
		(3, 4),
		(1, 5),
		(2, 5),
		(3, 5)
	], 
	(0, 0, 0, 255)
)
ImageDraw.Draw(numbers[4]).point(
	[
		(1, 1),
		(1, 2),
		(1, 3),
		(2, 3),
		(3, 3),
		(3, 2),
		(3, 1),
		(3, 4),
		(3, 5)
	], 
	(0, 0, 0, 255)
)
ImageDraw.Draw(numbers[5]).point(
	[
		(1, 1),
		(2, 1),
		(3, 1),
		(1, 2),
		(3, 3),
		(2, 3),
		(1, 3),
		(3, 4),
		(1, 5),
		(2, 5),
		(3, 5)
	], 
	(0, 0, 0, 255)
)
ImageDraw.Draw(numbers[6]).point(
	[
		(1, 1),
		(2, 1),
		(3, 1),
		(1, 2),
		(3, 3),
		(2, 3),
		(1, 3),
		(3, 4),
		(1, 5),
		(2, 5),
		(3, 5),
		(1, 4)
	], 
	(0, 0, 0, 255)
)
ImageDraw.Draw(numbers[7]).point(
	[
		(1, 1),
		(2, 1),
		(3, 1),
		(3, 2),
		(3, 3),
		(3, 4),
		(3, 5)
	], 
	(0, 0, 0, 255)
)
ImageDraw.Draw(numbers[8]).point(
	[
		(1, 1),
		(2, 1),
		(3, 1),
		(1, 2),
		(3, 3),
		(2, 3),
		(1, 3),
		(3, 4),
		(1, 5),
		(2, 5),
		(3, 5),
		(1, 4),
		(3, 2)
	], 
	(0, 0, 0, 255)
)
ImageDraw.Draw(numbers[9]).point(
	[
		(1, 1),
		(1, 2),
		(1, 3),
		(2, 3),
		(3, 3),
		(3, 2),
		(3, 1),
		(3, 4),
		(3, 5),
		(2, 1)
	], 
	(0, 0, 0, 255)
)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("path",         help="the file to modify",      type=str)
	parser.add_argument("frame_width",  help="the width of one frame",  type=int)
	parser.add_argument("frame_height", help="the height of one frame", type=int)
	parser.add_argument("mode",         help="choose between output modes (checker/ribbon/grid)", type=str)
	args = parser.parse_args()

	clip_w = args.frame_width
	clip_h = args.frame_height

	sheet = Image.open(args.path).convert("RGBA")

	grid = Image.new("RGBA", sheet.size, (255, 255, 255, 0))
	draw = ImageDraw.Draw(grid)

	if args.mode and args.mode == "checker":
		for row in range(0, grid.height, clip_h):
			for col in range(0, grid.width, clip_w):
				if (row / clip_h + col / clip_w) % 2 == 0:
					draw.rectangle([(col, row), (col + clip_w, row + clip_h)], fill=(0, 0, 0, 32), outline=None, width=0)

	elif args.mode and args.mode == "ribbon":
		for row in range(clip_h, grid.height, clip_h * 2):
			draw.rectangle([(0, row), (grid.width, row + clip_h)], (96, 0, 0, 48))

		for col in range(clip_w, grid.width, clip_w * 2):
			draw.rectangle([(col, 0), (col + clip_w, grid.height)], (0, 96, 0, 48))

	else:
		for y in range(clip_h, grid.height, clip_h):
			draw.line([(0, y), (grid.width, y)], (0, 0, 0, 64), 1)

		for x in range(clip_w, grid.width, clip_w):
			draw.line([(x, 0), (x, grid.height)], (0, 0, 0, 64), 1)

	blend = Image.alpha_composite(grid, sheet)

	indices = Image.new("RGBA", (grid.width + clip_w, grid.height + clip_h), (255, 255, 255, 0))
	for x in range(0, floor(indices.width / clip_w)):
		num_digits = len(str(x))
		index_image = Image.new("RGBA", (number_width * num_digits, number_height))
		for digit in range(num_digits):
			this_digit = int(str(x)[digit])
			index_image.paste(numbers[this_digit], (number_width * digit, 0))
		padding = 2
		index_image = index_image.resize((clip_w - padding, clip_h))
		indices.paste(index_image, (clip_w + padding + x * clip_w, 0))
	for y in range(0, floor(indices.height / clip_h)):
		num_digits = len(str(y))
		index_image = Image.new("RGBA", (number_width * num_digits, number_height))
		for digit in range(num_digits):
			this_digit = int(str(y)[digit])
			index_image.paste(numbers[this_digit], (number_width * digit, 0))
		padding = 2
		index_image = index_image.resize((clip_w - padding, clip_h))
		indices.paste(index_image, (0, clip_h + padding + y * clip_h))

	indices.paste(blend, (clip_w, clip_h))
	indices.save(args.path[0:args.path.rfind(".")] + "_AID" + args.path[args.path.rfind("."):], "PNG")

if __name__ == "__main__":
	main()