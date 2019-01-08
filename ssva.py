import argparse
from PIL import Image, ImageDraw

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

	out = Image.alpha_composite(grid, sheet)
	out.save(args.path[0:args.path.rfind(".")] + "_AID" + args.path[args.path.rfind("."):], "PNG")

if __name__ == "__main__":
	main()