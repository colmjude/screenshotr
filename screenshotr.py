#!/usr/bin/env python3

import asyncio
import os

import click
import pyppeteer
from PIL import Image, ImageDraw, ImageFont

# set this is be version I have installed
pyppeteer.__chromium_revision__ = 1000090

font_folder = "/Library/Fonts/"
system_fonts_foler = "/System/Library/Fonts/"

font_name = "HelveticaNeue.ttc"

font_size = 19
margin = 15

draw = None


@click.group()
def cli():
    pass


def add_text(img, text):
    pass


def add_text_container(draw, img_size, txt_size):
    ow, oh = img_size
    rh = txt_size[1] + (2 * margin)
    rw = txt_size[0] + (2 * margin)
    draw.rectangle((0, (oh - rh - 10), (rw + 10), oh), fill="#0b0c0c")
    draw.rectangle((5, (oh - rh - 5), (rw + 5), (oh - 5)), fill="white")
    return (0, (oh - rh - 10), (rw + 10), oh)


def add_url_to_img(url, screenshot):
    img = Image.open(screenshot)
    ow, oh = img.size
    draw = ImageDraw.Draw(img)

    txt_str = f"Screenshot from:\n{url}"

    chosen_font = ImageFont.truetype(os.path.join(system_fonts_foler, font_name), 19)
    size = draw.textsize(txt_str, chosen_font)
    container = add_text_container(draw, img.size, size)

    draw.text(
        (container[0] + 20, container[1] + 20),
        txt_str,
        fill="#0b0c0c",
        font=chosen_font,
    )
    # draw.text((15,15), txt_str, fill='#0b0c0c', font=chosen_font)
    img.save(screenshot)


async def screenshotr(url, output, fullPage, width, height, saveurl):
    browser = None
    page = None
    if browser is None:
        browser = await pyppeteer.launch({"args": ["--no-sandbox"]})
    if page is None:
        page = await browser.newPage()

    screenshot_path = f"screenshots/{output}.png"

    if not os.path.isdir("screenshots"):
        os.mkdir("screenshots")

    # default setting
    # sets the page size for non fullpage screenshots
    await page.setViewport({"width": width, "height": height, "deviceScaleFactor": 2.0})

    vp = page.viewport
    print(vp)
    print("chromium version")
    print(pyppeteer.__chromium_revision__)
    await page.emulateMedia("screen")

    await page.goto(url, {"waitUntil": "networkidle0"})

    # await page.waitForSelector("img") - might fail if no img on page
    await page.waitFor(1000)

    dimensions = await page.evaluate(
        """() => {
        return {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight,
            deviceScaleFactor: window.devicePixelRatio,
            userAgent: window.navigator.userAgent,
            fullpageHeight: document.documentElement.offsetHeight
        }
        }"""
    )
    print(dimensions)
    print(dimensions["fullpageHeight"])

    fp = fullPage in ["t", "true", "T", "True", True]

    opts = {"path": screenshot_path, "type": "png"}
    click.echo(opts)
    if fp:
        # need to calculate and use the max height
        # because fullpage option seems to make it too long (xN height)

        # resize viewport to be max height
        await page.setViewport(
            {
                "width": width,
                "height": dimensions["fullpageHeight"],
                "deviceScaleFactor": 2.0,
            }
        )

    # if not fullPage:
    #     opts['clip'] = {
    #         'x': 0,
    #         'y': 0,
    #         'width': 1000,
    #         'height': 1600
    #     }

    await page.screenshot(opts)

    await browser.close()

    if saveurl:
        add_url_to_img(url, screenshot_path)


@cli.command()
@click.option("--url")
@click.option("--vwidth", default=1200)
@click.option("--vheight", default=1600)
@click.option("--output", default="screenshot.png")
@click.option("--fullpage", default=False)
@click.option("--saveurl", default=True)
def screenshot(url, vwidth, vheight, output, fullpage, saveurl):
    click.echo("Capturing screenshot…")
    if url is None:
        click.echo("Aborting - No url provided")
        return False
    asyncio.get_event_loop().run_until_complete(
        screenshotr(
            url=url,
            output=output,
            fullPage=fullpage,
            width=vwidth,
            height=vheight,
            saveurl=saveurl,
        )
    )
    click.echo("Done")


if __name__ == "__main__":
    cli()
