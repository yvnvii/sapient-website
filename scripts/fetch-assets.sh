#!/usr/bin/env bash
#
# Downloads every image and PDF from the live Wix site into the right place
# in this project, at original resolution.
#
#   bash scripts/fetch-assets.sh
#
# Run it from the project root, WHILE THE WIX SITE IS STILL LIVE. Once the
# subscription lapses these URLs stop working and the files are gone.
#
# Wix serves resized copies under /v1/fill/... — these URLs have that part
# stripped off, so you get the originals.

set -u
cd "$(dirname "$0")/.." || exit 1

M="https://static.wixstatic.com/media"
F="https://www.sapientjournal.com/_files/ugd"

ok=0
fail=0

get () { # get <url> <destination>
  mkdir -p "$(dirname "$2")"
  if curl -fsSL --retry 2 -o "$2" "$1"; then
    printf '  ok   %s\n' "$2"; ok=$((ok+1))
  else
    printf '  FAIL %s\n' "$2"; fail=$((fail+1))
  fi
}

echo "Volume PDFs..."
get "$F/34c5a2_3a28172dc6924bcd9724c01338a6b68d.pdf" public/files/sapient-vol-13.pdf
get "$F/34c5a2_faacfd7c04a84de6a1145f9d266d69ab.pdf" public/files/sapient-vol-12.pdf
get "$F/34c5a2_b63ea3085c8843c783cf671186e398aa.pdf" public/files/sapient-vol-11.pdf
get "$F/34c5a2_014de1092f6b4c6780f5472103681b8c.pdf" public/files/sapient-vol-10.pdf
get "$F/34c5a2_dacfbc277ed74eb9b87f8433c4ca5815.pdf" public/files/sapient-vol-9.pdf
get "$F/34c5a2_e7e96bc5ea0f47bf897b49904dd80baa.pdf" public/files/sapient-flyer.pdf

echo "Brand and page images..."
get "$M/34c5a2_aa12d89bd73c42799bbd81e3261e8d89~mv2_d_2912_4030_s_4_2.jpg" public/images/logo-monkey-selfie.jpg
get "$M/34c5a2_481d927f9eb7446ea8b6978529f43759~mv2.png" public/images/columbia-logo.png
get "$M/34c5a2_02d55d8cb2b846889d97ff138404ba6e~mv2.png" public/images/e3b-logo.png
get "$M/d4be348333ab4747ba38dfcc28bd1901.jpg" public/images/hero-background.jpg
get "$M/34c5a2_64f73a0e022543d4a0f63663f133bb99~mv2.jpg" public/images/meet-the-team.jpg
get "$M/34c5a2_a038fcb4d313446ab741b58ec18b0f1c~mv2_d_3811_2569_s_4_2.jpg" public/images/letter-from-editor.jpg
get "$M/11062b_68b4fdb6b17e43898d117d206f5fa001~mv2_d_4500_3000_s_4_2.jpg" public/images/why-peer-review.jpg
get "$M/34c5a2_c7ebe9bef9fa4a3e9dfc01bb1c39a611~mv2.jpg" public/images/why-platform.jpg
get "$M/34c5a2_7279c309710f4e72bc145d8d0bd2bc96~mv2.jpg" public/images/why-leadership.jpg
get "$M/34c5a2_15f1fdebaf8744e584f5fba2a7c0a013~mv2.jpg" public/images/questions.jpg

echo "Volume 13 cover..."
get "$M/34c5a2_7847497e24b04a3fb85ea60ca2f74dfe~mv2.png" public/images/covers/vol-13.png

echo "Board photos..."
get "$M/34c5a2_fe015857504b48feb6f38d9ed76bf58f~mv2.jpeg" public/images/board/janaki-nair.jpg
get "$M/34c5a2_e0ec0f96ce08467e9809923a3c594bc3~mv2.jpg"  public/images/board/yuki-ogawa.jpg
get "$M/34c5a2_607c6209705e4f38ad12d697bae69e4e~mv2.jpg"  public/images/board/shane-nishimura.jpg
get "$M/34c5a2_e17ca21bbd694b0a822553ababbbe612~mv2.jpg"  public/images/board/charlotte-gravlee.jpg
get "$M/34c5a2_eef28fa877924a13b2b71e6f81e71fce~mv2.jpeg" public/images/board/joanna-lin.jpg
get "$M/34c5a2_886d972b84814cbca1fc0264f9298ee4~mv2.jpg"  public/images/board/emi-gacaj.jpg
get "$M/34c5a2_fbd1917d6f964077a23fd86086059717~mv2.jpg"  public/images/board/alix-draper.jpg
get "$M/34c5a2_1bbce886f87d41e9804e1b5bb82f7eac~mv2.jpg"  public/images/board/ray-atlas.jpg
get "$M/34c5a2_f81241cb700c43248fa6acc4a18ac759~mv2.png"  public/images/board/default-pfp.png

echo "Alumni photos..."
get "$M/34c5a2_37f390121d424487be94812b7473f0ca~mv2.jpg" public/images/board/ana-reif.jpg
get "$M/34c5a2_fdc54335f7d247ca898d5a1d57b82c96~mv2.jpg" public/images/board/lily-kuhn.jpg
get "$M/34c5a2_fbdef50ebbf149a08588a2f109ff793e~mv2.jpg" public/images/board/rahele-megosha.jpg
get "$M/34c5a2_99d3022da43743c0b1c2c17d888b57c8~mv2.jpg" public/images/board/adam-vogt.jpg
get "$M/34c5a2_5de80616bdc2400c931a174ecc2e9a7d~mv2.jpg" public/images/board/charla-teves.jpg
get "$M/34c5a2_df6168c637d545f7b30167ddc30a7088~mv2.png" public/images/board/jill-shapiro.png

echo "Blog post images..."
get "$M/ca8209_3cd3c15bb1494e5381d8e2731322ae01~mv2.jpg"  public/images/posts/in-the-news-new-paranthropus-robustus-fossils-discovered-in-south-africa.jpg
get "$M/ca8209_b29b647fae244038a5b94018f13acfdf~mv2.avif" public/images/posts/in-the-news-a-dying-dialect-among-wild-west-chimpanzees.jpg
get "$M/34c5a2_c3bfe20e05a249dcb34a991b54408c0c~mv2.png"  public/images/posts/scavenging-a-home-how-ice-age-humans-built-houses-from-mammoth-bones.jpg
get "$M/34c5a2_ee2419043b524dc8a3d8a24b43812a3e~mv2.png"  public/images/posts/primate-of-the-week-the-crowned-sifaka-propithecus-coronatus.jpg

echo
echo "Done: $ok downloaded, $fail failed."
echo
echo "Still needs doing by hand (Wix renders these as CSS backgrounds, so"
echo "there is no URL to grab — right-click and Save Image on the live site):"
echo "  public/images/monkey-portrait-1.jpg   the two round monkey photos"
echo "  public/images/monkey-portrait-2.jpg   beside the sa-pi-ent definition"
echo "  public/images/topics/topic-1..4.jpg   the four Research Topics circles"
echo "  public/images/covers/vol-9..12.png    older covers: use page 1 of each PDF"
