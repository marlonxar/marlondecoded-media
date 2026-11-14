from PIL import Image, ImageDraw, ImageFont
W,H=1080,1920
img=Image.new("RGBA",(W,H),(0,0,0,0))
d=ImageDraw.Draw(img)
# soft bottom gradient for legibility
for y in range(1180,1700):
    a=int(150*min(1,(y-1180)/220)*(1 if y<1560 else max(0,(1700-y)/140)))
    d.line([(0,y),(W,y)],fill=(0,0,0,a))
f=ImageFont.truetype("/mnt/skills/examples/canvas-design/canvas-fonts/BigShoulders-Bold.ttf",78)
txt="NEW REEL ON MY PROFILE"
tw=d.textlength(txt,font=f)
emo=Image.new("RGBA",(160,160),(0,0,0,0))
ImageDraw.Draw(emo).text((0,0),"👆",font=ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",109),embedded_color=True)
emo=emo.crop(emo.getbbox()).resize((80,80),Image.LANCZOS)
gap=24; padx=56; pady=34
bw=int(tw+gap+80+2*padx); bh=128
x0=(W-bw)//2; y0=1400
d.rounded_rectangle([x0+8,y0+10,x0+bw+8,y0+bh+10],radius=64,fill=(0,0,0,120))
d.rounded_rectangle([x0,y0,x0+bw,y0+bh],radius=64,fill=(255,255,255,255))
d.text((x0+padx,y0+bh//2),txt,font=f,fill=(17,17,17,255),anchor="lm")
img.alpha_composite(emo,(int(x0+padx+tw+gap),y0+(bh-80)//2))
f2=ImageFont.truetype("/mnt/skills/examples/canvas-design/canvas-fonts/BigShoulders-Bold.ttf",52)
d.text((W//2,y0+bh+56),"@marlondecoded · tap my name",font=f2,fill=(255,255,255,235),anchor="mm")
img.save("story_banner.png")
