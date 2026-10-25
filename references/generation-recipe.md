# 可复用生成配方与复现记录

使用前先读取本款商品锁定卡。下文根据已完成并经过视觉检查的单款三视图提炼为 `natural-window-v3`；新款仍须逐图核对实拍。只替换有证据的字段，不把短绒或米白搭配套用于所有款式。当前人物字段是用户指定预设，不能自动退回此前的短发人物。方括号是编写时占位符，调用工具前必须填写或移除。

## A. 正面基准：先商品，再摄影参考

参考顺序：
1. 商品正面。
2. 商品背面。
3. 可选真人摄影参考，明确只借鉴头发、肤质或成像。
4. 可选第二张补充摄影参考。

若用户指定某人身份，另列身份参考并明确优先级，将模板里的虚构人物描述替换为该身份约束；摄影氛围参考不自动授权换脸。没有额外真人图片也可按默认配方生成，不因缺风格图阻塞。

英文模板：

```text
Create a NEW honest, unretouched full-body fashion photograph in natural
window daylight, FRONT view, vertical 2:3, complete head and shoes with
moderate margins. Candid fashion editorial photography, soft contrast,
realistic skin texture, natural color grading and authentic fabric textures.

INPUT ROLES:
Image 1: actual garment FRONT, exact product to wear.
Image 2: actual garment BACK, exact product construction and surface.
[Image 3/4: photographic references ONLY for casual unstyled hair,
natural skin texture with restrained highlights and understated camera rendering.
Do not copy those persons' identities, clothing, backgrounds, text or watermarks.]

SUBJECT:
One fictional YOUNG ADULT woman, [explicit adult age], healthy slim natural
proportions. Slightly elongated oval face, slender nose bridge, naturally
dense brown eyebrows, gray-brown eyes, nude rose lips. Fair skin with a
natural pink undertone, mildly flushed cheeks, faint under-eye shadows.
Light sheer natural makeup, visible skin texture at this viewing distance,
soft natural sheen on forehead and nose bridge. No exaggerated translucency,
beauty glow, glossy cheek highlighter, skin smoothing or artificial aging.
A tiny dark beauty mark beside the nose on HER ANATOMICAL LEFT: it appears
on image-right in an unmirrored frontal portrait. Keep its anatomical side;
do not move or duplicate it when the face turns. It may naturally be hidden.
Deep chestnut-brown medium-length hair, near-center part, loosely and casually
pinned in a loose low updo at the back, airy volume at crown, slightly disheveled.
Thin irregular long wisps over forehead; one curved strand descends from near
the space between the eyebrows toward the side of the nose. Loose side
strands fall along cheeks and neck, some reaching the collar. Fine natural
flyaways, irregular density and bends; no symmetrical curls or halo of loops.
Maintain the loose updo from all views, and keep essential garment construction
visible. [Selected accessories.] Relaxed eyelids, mouth and ordinary soft
eye reflections. Do not force extra freckles or scars.

GARMENT - HIGHEST PRIORITY:
[Exact visible structure, front/back differences, closure and wearing state.]
[Observed color relationships, material surface, nap/weave scale,
true pattern or absence of pattern, highlight width/intensity, natural folds.]
Match the actual sample's MATERIAL, COLOR RELATIONSHIPS, PATTERN and
REFLECTANCE. Preserve pattern scale, density, direction, placement and joins.
Skin finish and film grain must not alter clothing: preserve satin, leather,
metallic or other real garment highlights when present. Window light may
move highlights naturally; it must not change the material or dye color.
[Specific forbidden material/structure drift for THIS item.]

STYLING AND POSE:
[Complete complementary outfit, shoes/accessories and colors.]
Shoulders relaxed, torso front-facing, a modest weight shift or small step.
Hands and hair do not cover the garment's important construction.

ROOM, DAYLIGHT AND CAMERA:
Minimal indoor setting with a neutral dark gray backdrop and plain smooth
gray floor. One fixed window at camera left/front supplies natural daylight;
the window can stay outside the frame. Preserve ordinary room light falloff,
the naturally darker far side and soft ambient/contact shadows.
Only existing weak room reflections: no added fill lights, artificial studio
lighting, softboxes, beauty lights, reflector setup or rimlight.
No HDR shadow lifting; soft contrast does not mean removing all shadows.
Faithful garment colors and natural color grading, no strong warm/cool cast.
Realistic 85mm-like perspective, enough depth for the complete outfit.
Subtle fine film-grain appearance, slight optical softness and gentle tonal
transitions, no excessive retouching or sharpening halos. Grain is an image
characteristic, never new fabric pattern or floor relief. Keep source fabric
grain, seams, true printed motifs and shoes readable.
The floor remains plain: no carpet, embossed relief, swirls or worm-like marks.

One independent photograph. Preserve genuine text, labels or logos that
belong to the actual garment; do not invent or alter them. No added captions,
view labels, watermarks, borrowed reference branding, frame or collage.
```

只有无图案短绒/绒面时才加入以下材料句，其他材料按锁定卡替换：

```text
PLAIN UNPATTERNED short-nap suede-like surface with broad diffuse cloudy
tone changes from nap direction, like the actual garment.
No decorative lines, paisley, swirls, floral print, embossing or cracks.
```

## B. 背面与侧面：使用通过的基准

固定参考顺序：
1. 已验收正面，定义同一人物、头发、搭配、穿法、光线和成像。
2. 原始商品背面。
3. 原始商品正面。

已有侧面实拍时追加并明确其角色。不要把失败的旧背/侧图当作材质依据。新生成基准换了人物或光场时，背、侧必须配套重建。

共用模板：

```text
Create ONE full-body photograph from the SAME adult model, SAME outfit and
SAME natural-window-daylight indoor session as image 1.
Image 1 is the approved identity, hair, wardrobe, lighting and camera-finish
anchor. Images 2 and 3 are actual garment back/front and remain authoritative
for product structure, color, material and reflectance.

Keep [specific identity/hair anchors], [selected individual skin details],
[complete outfit and accessories], [closures and wearing state].
Retain the chestnut near-center-part loose low updo, crown volume, forehead
strand and cheek/neck wisps from the approved front. Preserve gray-brown
eyes, nude rose lips, fair pink skin, mild cheek redness and faint under-eye
tone; retain soft natural forehead/nose highlights, not beauty translucency.
The tiny perinasal mole stays on HER ANATOMICAL LEFT. Show it only when that
region is visible; never mirror the face or move the mole to the visible side.
Keep relaxed expression, realistic skin and natural optical transitions.
Do not add glossy coiffure, glassy eyes, heavy freckles, smoothing or aging.

GARMENT: [repeat complete item-specific structure AND material lock].
Respect actual BACK construction; do not place the front zipper/pockets
on the back or invent seams. Infer unseen side connections conservatively.

Same neutral dark gray indoor setting, smooth gray floor and fixed window
at camera left/front. Choose the camera position and base exposure before approving the front.
After approval the camera and window stay in place; only the model turns.
Exposure may be adjusted moderately for garment readability without shifting
its colors, lifting all shadows or changing the required clothing view.
Allow the face and fabric shadows/highlight positions to change with rotation.
Only natural weak room reflections, no added fill or artificial studio lights.
Keep normal room shadow depth, natural colors, faithful garment reflectance
and real pattern scale/placement. Soft contrast, subtle fine film grain,
slight optical softness without blurring fabric motifs, seams or shoes.
No HDR or excessive retouching. Same full-body scale, camera height and
2:3 intent; head and shoes complete.

[Append ONE angle instruction below.]
Preserve genuine text/marks belonging to the actual garment. No added captions,
view labels, watermarks, reference-image branding, border or collage.
```

背面追加：

```text
BACK VIEW: back of shoulders and hips face the camera; display the complete
back panel. Hair must not hide essential collar/back construction.
Allow a slight head turn and subtle weight shift, arms naturally clear
of the garment. Show full rear hem and shoes. This is a rear clothing view,
not a front view with the head turned.
```

侧面追加：

```text
SIDE VIEW: near 90-degree profile, face and torso toward [IMAGE RIGHT/LEFT].
A gentle small step or relaxed standing profile; arms do not conceal
the side silhouette. Keep the approved face identity, hair and clothing
volume, full trousers/skirt and shoes. No front three-quarter substitution.
Do not force the left-side nasal mole to appear if the right cheek is visible.
```

## C. 迭代顺序与停止条件

1. 看衣服：图案有无、绒毛/织纹、反光和结构不对，先修衣服，不接受“人像更真”的抵偿。
2. 看人像：先检查指定五官、松挽发和左鼻旁痣，再调过强高光与过整齐头发；保留额头和鼻梁的正常自然光泽。不强加新雀斑，不把纹理理解为往光滑脸上撒点。
3. 看光场：固定窗位、正常室内亮暗、正确接触影和中性灰环境；不靠四面补光抹掉阴影，人物转身后高光允许自然移动，但不能改变衣料类别、颜色或花纹。
4. 最后看成像：适当细胶片颗粒与轻微光学柔化，不变成实体表面纹理，不磨皮或损坏花纹、缝线与鞋履可读性。
5. 正面不通过不扩展另外两角度。通过后锁定其实际文件，而非仅重用一句外貌描述。
6. 局部修正重复失败或伪纹加重时，从原实拍重新建立；不要递归强化已失真的底图。遵循SKILL.md中的单款修正预算，未解决要明确报告。

参考中可能出现精修、强妆、压缩和硬光。只记录实际看见的特征；不能从JPEG里的噪点推断真实相机或把雀斑当作毛孔。禁止在提示词中同时追求“每根汗毛极致锐利”和粗颗粒全身照。

## D. 复现档案

区分两个目标：
- **重建既有PDF**：保存已通过图片、原始实拍、清单、排版脚本版本和字体；可重建同样的内容与版面。不承诺PDF文件字节一致（元数据等可能不同）。
- **重新生成相似影像**：保存完整输入与提示词，以复用人物/摄影规则；工具的随机性或版本变化可能改变结果。未返回的seed/model/ISO不得填写猜测值。

每款在批次目录存 `generation-record.json` 或等价结构，至少包括：

```json
{
  "style_id": "USER_STYLE_ID",
  "visual_profile": "natural-window-v3",
  "tool": "image_gen",
  "inputs": [
    {"role": "garment_front", "path": "sources/front.jpg", "sha256": "COMPUTED_FROM_FILE"},
    {"role": "garment_back", "path": "sources/back.jpg", "sha256": "COMPUTED_FROM_FILE"},
    {"role": "photographic_style_only", "path": "references/style.jpg", "sha256": "COMPUTED_FROM_FILE"}
  ],
  "garment_lock": {
    "structure": [],
    "surface": "",
    "reflectance": "",
    "pattern": "",
    "color_relationships": "",
    "forbidden_drift": [],
    "uncertain": []
  },
  "identity_anchor": {
    "approved_front": "approved/front.png",
    "features": [],
    "individual_skin_details": [],
    "mole_location": "anatomical_left_perinasal; image-right in unmirrored front",
    "hair_structure": "medium-length chestnut hair loosely pinned up at back"
  },
  "outfit": [],
  "wearing_state": {},
  "scene": {
    "background": "neutral dark gray indoor backdrop",
    "floor": "plain smooth gray",
    "key_light": "natural daylight from a fixed window at camera-left/front",
    "fill": "existing weak room reflections only; no added fill or studio lights",
    "camera_language": "realistic 85mm-like full-body perspective",
    "grain": "subtle fine film-grain appearance",
    "softness": "slight optical softness; preserve true fabric and skin detail",
    "shadow_behavior": "camera and window fixed; model rotates"
  },
  "side_inferred": true,
  "generations": [
    {
      "view": "front",
      "prompt_file": "prompts/front-01.txt",
      "reference_roles_in_order": ["garment_front", "garment_back", "photographic_style_only"],
      "result_path": "approved/front.png",
      "actual_pixels": [1024, 1536],
      "status": "accepted",
      "review": []
    }
  ],
  "pdf_manifest": "manifest.json",
  "pdf_language": "bilingual"
}
```

这是结构示例，值必须按当前实际数据填写；缺少风格图时删除该输入项，输出尺寸读取真实文件。记录每个视角的身体/头部朝向和痣的可见性，不把画面左右当成人物左右。对背面、侧面和每次修正追加各自完整记录，保存最终引用次序、失败原因与替代关系；不只保存“同上”或省略后的提示词。哈希可用PowerShell `Get-FileHash -Algorithm SHA256 -LiteralPath ...` 或Python计算。

批准图片、原始图片和所用风格图放稳定路径，清单尽量用相对路径；保留文件哈希、日期及工具实际返回的标识（如果有）。把内部记录放档案或附属包，展示PDF仍只含款号与中英双语视角。
