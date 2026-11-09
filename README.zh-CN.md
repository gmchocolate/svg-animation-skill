# SVG Animation Skill · 参考驱动的网页动效创作技能

**让 AI 学会动画设计，而不只是生成会动的代码。**

这是一个可安装的 Agent Skill，供你在日常网页设计、产品开发、Nuxt/Vue、品牌官网、交互组件和数据可视化中反复调用。

## 核心理念

优秀动画不只是平移、旋转和发光，而是通过**出现顺序、速度、缓动、轨迹、节奏与停顿**引导用户理解页面。

完整流程：

**了解当前网页 → 查看真实参考动效 → 提取运动规律 → 设计分镜 → 生成可编辑的 SVG 动画代码 → 在浏览器验证 → 迭代打磨。**

能力包括：
- **参考学习**：真正查看 SVG/GIF/MP4/WebM 等动效，不把静态封面当作运动观察结果。
- **私人审美库**：经过用户明确允许，保存真实参考文件及偏好到本地 ~/.svg-animation-skill/；不自动上传 GitHub。
- **网页适配**：先读主题、字体、现有组件、断点和依赖；生成与网站协调的动效，而不是炫技。
- **按需选型**：优先 SVG + CSS，必要时采用 Anime.js、GSAP、Motion、SVG.js。
- **可交付代码**：生成 SVG、CSS、Vue/Nuxt 组件；不拿一张动效截图冒充实现。
- **质量把关**：考虑减少动画偏好、SSR、移动端、图形清晰度、性能、停止/清理和事实准确性。

## 安装

~~~bash
npx skills add gmchocolate/svg-animation-skill
~~~

Skill 入口是 [skills/svg-animation/SKILL.md](skills/svg-animation/SKILL.md)。安装后可在支持 Agent Skills 的本地编码 Agent 中使用；宿主必须有相应的文件访问与浏览器/视频工具，才能真正观看动效参考。

## 日常使用

直接对支持 Skill 的 AI 编码助手说：

> 使用 svg-animation，先看一下当前页面的主题、布局和设计语言，为首页 Hero 做一段高级、克制的 SVG 动画。优先借鉴我的本地参考动效，输出 Vue 组件，并在浏览器检查移动端和减少动画模式。

或者：

> 分析这段动效最值得借鉴的节奏与图形运动规律；在我同意后存入本地动效参考库，以后创作时自动优先参考。

以及：

> 现在的动画太花哨了，帮我找出注意力竞争、动画节奏和性能方面的问题，按高级 SaaS 官网的审美重做。

## 建立本地参考库

Python 3.10+，无需额外 Python 依赖。从 skills/svg-animation/ 目录运行：

~~~bash
python scripts/motion_library.py add \
  --file "/path/to/inspiration.svg" \
  --title "极简路径生长" \
  --use-case hero \
  --tag minimal --tag line-drawing \
  --like "先出现主结构，再出现联系线" \
  --avoid "持续闪烁、无意义粒子" \
  --rating 5

python scripts/motion_library.py list
python scripts/motion_library.py select --use-case hero --top 2
python scripts/motion_library.py prepare --use-case hero --request "创作简洁的 SaaS Hero 动画"
~~~

参考资料仍在**实际运行这个命令的机器**上；远端云 Agent 无法凭空读取你笔记本中的私人文件。CLI 不使用网络，不训练模型，不自动生成作品。静态图片只能给出视觉风格，不能代表完整动画节奏。

## 代码检查

~~~bash
python skills/svg-animation/scripts/check_svg.py skills/svg-animation/examples/line-draw.svg
python -m unittest discover -s tests -v
~~~

静态检查无法代替浏览器实际观看。质量标准参见 [动效质量评审](skills/svg-animation/references/quality-gates.md)。

## 仓库内容

- [Skill 完整执行规范](skills/svg-animation/SKILL.md)
- [参考优先创作流程](skills/svg-animation/references/reference-first-workflow.md)
- [运动语法与编排](skills/svg-animation/references/motion-grammar.md)
- [动画技术选型](skills/svg-animation/references/runtime-selection.md)
- [Vue/Nuxt 集成](skills/svg-animation/references/nuxt-vue.md)
- [质量检查](skills/svg-animation/references/quality-gates.md)
- [本地私人动效库](skills/svg-animation/references/local-taste-library.md)

本项目代码和文档使用 MIT 协议；第三方参考作品不自动获得转载或分发许可。GSAP 等外部库适用各自许可证。
