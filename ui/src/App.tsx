import { useState, useCallback } from "react";
import {
  Upload, Sparkles, Image as ImageIcon, Settings2, ChevronDown, ChevronUp,
  RefreshCw, Download, AlertTriangle, Check, X, Loader2, Trash2, Pencil,
  Palette, ArrowRight,
} from "lucide-react";

type Step = "upload" | "analyzing" | "planning" | "generating" | "complete";

interface ShotBrief { title: string; description: string; content: string; expanded: boolean; }
interface GenImage { id: number; title: string; status: "pending" | "generating" | "done" | "failed"; score?: number; issue?: string; }

function Badge({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-medium border ${className}`}>{children}</span>;
}

function Select({ value, onChange, options, className = "" }: { value: string; onChange: (v: string) => void; options: { value: string; label: string }[]; className?: string }) {
  return (
    <select value={value} onChange={(e) => onChange(e.target.value)}
      className={`h-9 text-xs rounded-md border border-gray-200 bg-white px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 w-full ${className}`}>
      {options.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
    </select>
  );
}

export default function App() {
  const [images, setImages] = useState<string[]>([]);
  const [step, setStep] = useState<Step>("upload");
  const [imageCount, setImageCount] = useState(8);
  const [model, setModel] = useState("gemini-3-pro-image-preview");
  const [ratio, setRatio] = useState("1:1");
  const [resolution, setResolution] = useState("2K");
  const [language, setLanguage] = useState("none");
  const [planningModel, setPlanningModel] = useState("gemini-3-flash-preview");
  const [temperature, setTemperature] = useState("0.4");
  const [autoRetry, setAutoRetry] = useState(true);
  const [workers, setWorkers] = useState("8");
  const [variantDetection, setVariantDetection] = useState("auto");
  const [showNotes, setShowNotes] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [notes, setNotes] = useState("");
  const [specsExpanded, setSpecsExpanded] = useState(false);
  const [designSpecs, setDesignSpecs] = useState("");
  const [briefs, setBriefs] = useState<ShotBrief[]>([]);
  const [generated, setGenerated] = useState<GenImage[]>([]);
  const [variants, setVariants] = useState<{ name: string; active: boolean }[]>([]);

  const handleFiles = useCallback((files: FileList | File[]) => {
    Array.from(files).filter((f) => f.type.startsWith("image/")).forEach((file) => {
      const reader = new FileReader();
      reader.onload = (e) => setImages((prev) => [...prev.slice(0, 5), e.target?.result as string]);
      reader.readAsDataURL(file);
    });
  }, []);

  const scoreColor = (s: number) => s >= 85 ? "bg-emerald-500 text-white border-emerald-500" : s >= 70 ? "bg-amber-500 text-white border-amber-500" : "bg-red-500 text-white border-red-500";

  const stepList = [
    { key: "upload", label: "上传" }, { key: "analyzing", label: "分析中" },
    { key: "planning", label: "确认规划" }, { key: "generating", label: "生成中" },
    { key: "complete", label: "完成" },
  ];
  const stepIndex = stepList.findIndex((s) => s.key === step);

  const mockAnalyze = () => {
    setStep("analyzing");
    setTimeout(() => {
      setDesignSpecs("# 整体设计规范\n\n## 色彩系统\n- **主色调**：柔和粉色（#F4C2C2）\n- **辅助色**：香槟金（#D4AF37）、奶油白\n- **背景色**：温暖的米白色\n\n## 摄影风格\n- **光线**：侧向自然软光\n- **景深**：中浅景深\n- **相机参数**：f/2.8, 1/125s, ISO 100\n\n## 品质要求\n- 分辨率：4K/高清\n- 真实感：超写实/照片级");
      setVariants([{ name: "粉色", active: true }, { name: "米白", active: true }, { name: "薄荷绿", active: true }]);
      const titles = ["主视觉展示图", "内部结构展示图", "便携场景图", "多色集合图", "细节特写图", "旅行场景图", "礼品场景图", "尺寸对比图"];
      const descs = ["展示产品闭合状态的整体外观", "展示打开状态的收纳功能", "展示产品与手提包的比例", "展示三种颜色变体", "展示拉链和皮革质感", "展示旅行场景效果", "展示送礼场景", "展示与手掌大小对比"];
      setBriefs(titles.slice(0, imageCount).map((t, i) => ({ title: t, description: descs[i] || "", content: `**产品复杂结构判定**：true\n**选用视角**：45度斜角\n\n##图${i + 1}：${t}\n\n**设计目标**：${descs[i]}\n**产品出现**：是\n\n**构图方案**：\n• 产品占比：${50 + i * 5}%\n• 布局方式：居中偏右构图\n-文字区域：无文案区域`, expanded: false })));
      setStep("planning");
    }, 2500);
  };

  const mockGenerate = () => {
    setStep("generating");
    const imgs: GenImage[] = briefs.map((b, i) => ({ id: i, title: b.title, status: "pending" as const }));
    setGenerated(imgs);
    imgs.forEach((_, i) => {
      setTimeout(() => {
        setGenerated((prev) => prev.map((img, j) => j === i ? { ...img, status: "generating" } : img));
        setTimeout(() => {
          setGenerated((prev) => prev.map((img, j) => j === i ? { ...img, status: "done", score: Math.floor(Math.random() * 25) + 75, issue: Math.random() > 0.8 ? "产品厚度偏差" : undefined } : img));
          if (i === imgs.length - 1) setTimeout(() => setStep("complete"), 500);
        }, 1500);
      }, i * 2500);
    });
  };

  const reset = () => { setStep("upload"); setGenerated([]); setBriefs([]); setDesignSpecs(""); setVariants([]); };

  return (
    <div className="min-h-screen bg-[#F8FAFC] font-sans">
      {/* Header */}
      <header className="border-b border-gray-200 bg-white px-6 py-3 flex items-center justify-between shadow-sm">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-lg bg-blue-600 flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-white" />
          </div>
          <h1 className="text-lg font-bold tracking-tight">MercaFlow</h1>
          <Badge className="bg-white text-gray-600 border-gray-200">MercadoLibre</Badge>
        </div>
        <div className="flex items-center gap-2 text-xs text-gray-400">
          <span>Vertex AI</span>
          <div className="h-2 w-2 rounded-full bg-amber-400" />
        </div>
      </header>

      {/* Steps */}
      <div className="flex items-center justify-center gap-2 py-4 bg-white border-b border-gray-200">
        {stepList.map((s, i) => (
          <div key={s.key} className="flex items-center gap-2">
            <div className="flex items-center gap-1.5">
              <div className={`h-7 w-7 rounded-full flex items-center justify-center text-xs font-medium transition-all ${i < stepIndex ? "bg-blue-600 text-white" : i === stepIndex ? "bg-blue-600 text-white ring-4 ring-blue-100" : "bg-gray-100 text-gray-400"}`}>
                {i < stepIndex ? <Check className="w-3.5 h-3.5" /> : i + 1}
              </div>
              <span className={`text-xs font-medium ${i <= stepIndex ? "text-gray-900" : "text-gray-400"}`}>{s.label}</span>
            </div>
            {i < stepList.length - 1 && <div className={`h-px w-10 ${i < stepIndex ? "bg-blue-600" : "bg-gray-200"}`} />}
          </div>
        ))}
      </div>

      {/* Main */}
      <main className="grid grid-cols-1 lg:grid-cols-[360px_1fr] gap-6 p-6 max-w-[1440px] mx-auto">
        {/* LEFT */}
        <div className="flex flex-col gap-4">
          {/* Upload */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <div className="h-7 w-7 rounded-full bg-gray-100 flex items-center justify-center"><ImageIcon className="w-3.5 h-3.5 text-gray-500" /></div>
                <div><div className="text-sm font-semibold">产品图</div><div className="text-[11px] text-gray-400">上传清晰的产品图片</div></div>
              </div>
              <span className="text-xs text-gray-400 font-medium">{images.length}/6</span>
            </div>
            <div className="grid grid-cols-3 gap-2">
              {images.map((img, i) => (
                <div key={i} className="relative group aspect-square rounded-xl overflow-hidden border border-gray-200 bg-gray-50">
                  <img src={img} className="w-full h-full object-cover" alt="" />
                  <button onClick={() => setImages((p) => p.filter((_, j) => j !== i))} className="absolute top-1 right-1 h-5 w-5 rounded-full bg-black/50 text-white flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity hover:bg-red-500"><X className="w-3 h-3" /></button>
                  {i === 0 && <div className="absolute bottom-1 left-1 px-1.5 py-0.5 rounded bg-black/40 text-[9px] text-white font-medium">主图</div>}
                </div>
              ))}
              {images.length < 6 && (
                <label className="aspect-square rounded-xl border-2 border-dashed border-gray-200 flex flex-col items-center justify-center cursor-pointer hover:border-blue-400 hover:bg-blue-50/30 transition-all"
                  onDrop={(e) => { e.preventDefault(); handleFiles(e.dataTransfer.files); }} onDragOver={(e) => e.preventDefault()}>
                  <Upload className="w-5 h-5 text-gray-300 mb-1" /><span className="text-[11px] text-gray-400">上传</span>
                  <input type="file" accept="image/*" multiple className="hidden" onChange={(e) => e.target.files && handleFiles(e.target.files)} />
                </label>
              )}
            </div>
          </div>

          {/* Settings */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 space-y-4">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium">生成数量</label>
                <span className="text-sm text-blue-600 font-bold">{imageCount} 张</span>
              </div>
              <input type="range" min={3} max={10} value={imageCount} onChange={(e) => setImageCount(Number(e.target.value))} className="w-full accent-blue-600" />
            </div>
            <div className="h-px bg-gray-100" />
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1.5">
                <label className="text-xs font-medium text-gray-500">模型</label>
                <Select value={model} onChange={setModel} options={[
                  { value: "gemini-3-pro-image-preview", label: "Nano Banana Pro" },
                  { value: "gemini-3.1-flash-image-preview", label: "Nano Banana 2" },
                  { value: "gemini-2.5-flash-image", label: "Nano Banana" },
                ]} />
              </div>
              <div className="space-y-1.5">
                <label className="text-xs font-medium text-gray-500">比例</label>
                <Select value={ratio} onChange={setRatio} options={[
                  { value: "1:1", label: "1:1 正方形" }, { value: "3:4", label: "3:4 竖版" },
                  { value: "4:3", label: "4:3 横版" }, { value: "9:16", label: "9:16 竖屏" }, { value: "16:9", label: "16:9 宽屏" },
                ]} />
              </div>
              <div className="space-y-1.5">
                <label className="text-xs font-medium text-gray-500">清晰度</label>
                <Select value={resolution} onChange={setResolution} options={[
                  { value: "1K", label: "1K 标清" }, { value: "2K", label: "2K 高清" }, { value: "4K", label: "4K 超清" },
                ]} />
              </div>
              <div className="space-y-1.5">
                <label className="text-xs font-medium text-gray-500">语言</label>
                <Select value={language} onChange={setLanguage} options={[
                  { value: "none", label: "无文字(纯视觉)" }, { value: "zh-CN", label: "中文" },
                  { value: "es-MX", label: "西班牙语" }, { value: "en-US", label: "英语" }, { value: "pt-BR", label: "葡萄牙语" },
                ]} />
              </div>
            </div>
          </div>

          {/* Notes */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-4">
            <button onClick={() => setShowNotes(!showNotes)} className="flex items-center justify-between w-full text-sm text-gray-500 hover:text-gray-700">
              <span>补充说明（可选）</span>{showNotes ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </button>
            {showNotes && <textarea value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="例如：展示产品放在手提包旁边..." className="mt-3 w-full min-h-[80px] text-sm rounded-lg border border-gray-200 p-3 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500" />}
          </div>

          {/* Advanced */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-4">
            <button onClick={() => setShowAdvanced(!showAdvanced)} className="flex items-center justify-between w-full text-sm text-gray-500 hover:text-gray-700">
              <span>高级设置</span>{showAdvanced ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </button>
            {showAdvanced && (
              <div className="mt-3 space-y-3">
                <div className="space-y-1.5"><label className="text-xs font-medium text-gray-500">规划模型</label>
                  <Select value={planningModel} onChange={setPlanningModel} options={[{ value: "gemini-3-flash-preview", label: "Gemini 3 Flash（推荐）" }, { value: "gemini-3.1-pro-preview", label: "Gemini 3.1 Pro" }]} className="h-8" /></div>
                <div className="space-y-1.5"><label className="text-xs font-medium text-gray-500">变体检测</label>
                  <Select value={variantDetection} onChange={setVariantDetection} options={[{ value: "auto", label: "自动检测" }, { value: "off", label: "关闭" }, { value: "manual", label: "手动指定" }]} className="h-8" /></div>
                <div className="grid grid-cols-2 gap-3">
                  <div className="space-y-1.5"><label className="text-xs font-medium text-gray-500">Temperature</label>
                    <Select value={temperature} onChange={setTemperature} options={[{ value: "0.2", label: "0.2 保守" }, { value: "0.4", label: "0.4 推荐" }, { value: "0.7", label: "0.7 创意" }, { value: "1.0", label: "1.0 随机" }]} className="h-8" /></div>
                  <div className="space-y-1.5"><label className="text-xs font-medium text-gray-500">并行数</label>
                    <Select value={workers} onChange={setWorkers} options={[{ value: "5", label: "5" }, { value: "8", label: "8" }, { value: "15", label: "15" }, { value: "30", label: "30" }]} className="h-8" /></div>
                </div>
                <div className="flex items-center justify-between py-1">
                  <span className="text-xs font-medium text-gray-500">自动重试（分数&lt;70）</span>
                  <button onClick={() => setAutoRetry(!autoRetry)} className={`w-9 h-5 rounded-full transition-colors ${autoRetry ? "bg-blue-600" : "bg-gray-300"} relative`}>
                    <div className={`absolute top-0.5 w-4 h-4 rounded-full bg-white shadow-sm transition-transform ${autoRetry ? "translate-x-4" : "translate-x-0.5"}`} />
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Actions */}
          <div className="space-y-3">
            {step === "upload" ? (
              <button className="w-full h-14 bg-blue-600 hover:bg-blue-700 text-white text-base font-semibold rounded-2xl shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed" onClick={mockAnalyze} disabled={images.length === 0}>
                <Sparkles className="w-5 h-5" /> 分析产品
              </button>
            ) : step === "planning" ? (
              <>
                <button className="w-full h-14 bg-blue-600 hover:bg-blue-700 text-white text-base font-semibold rounded-2xl shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2" onClick={mockGenerate}>
                  <ArrowRight className="w-5 h-5" /> 确认生成 {imageCount} 张图片
                </button>
                <button className="w-full h-12 border border-gray-200 bg-white hover:bg-gray-50 text-gray-700 text-base rounded-2xl transition-all flex items-center justify-center gap-2" onClick={reset}>
                  ← 返回上一步
                </button>
              </>
            ) : step === "complete" ? (
              <button className="w-full h-14 bg-blue-600 hover:bg-blue-700 text-white text-base font-semibold rounded-2xl shadow-md transition-all flex items-center justify-center gap-2" onClick={reset}>
                <Sparkles className="w-5 h-5" /> 新产品
              </button>
            ) : (
              <button className="w-full h-14 bg-gray-400 text-white text-base font-semibold rounded-2xl flex items-center justify-center gap-2 cursor-not-allowed" disabled>
                <Loader2 className="w-5 h-5 animate-spin" /> {step === "analyzing" ? "分析中..." : "生成中..."}
              </button>
            )}
          </div>
        </div>

        {/* RIGHT */}
        <div className="bg-white rounded-2xl border border-gray-200 shadow-sm min-h-[600px]">
          <div className="p-5 border-b border-gray-100">
            <div className="flex items-center gap-2">
              <div className="h-7 w-7 rounded-full bg-gray-100 flex items-center justify-center"><Sparkles className="w-3.5 h-3.5 text-gray-500" /></div>
              <div><div className="text-sm font-semibold">{step === "complete" ? "生成完成" : "设计规划预览"}</div>
                <div className="text-[11px] text-gray-400">{step === "upload" ? "上传产品图片后自动生成" : "请确认设计规范和图片规划"}</div></div>
            </div>
          </div>
          <div className="p-5">
            {step === "upload" ? (
              <div className="flex flex-col items-center justify-center h-[450px] text-gray-300">
                <div className="h-16 w-16 rounded-2xl bg-gray-50 flex items-center justify-center mb-4"><Upload className="w-8 h-8" /></div>
                <p className="text-sm text-gray-400">上传产品图片开始</p>
                <p className="text-xs text-gray-300 mt-1">支持 JPG, PNG，最多6张</p>
              </div>
            ) : (
              <div className="space-y-5">
                {/* Variants */}
                {variants.length > 0 && (
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="text-xs text-gray-500 font-medium">检测到变体:</span>
                    {variants.map((v, i) => (
                      <button key={i} onClick={() => setVariants((p) => p.map((vv, j) => j === i ? { ...vv, active: !vv.active } : vv))}
                        className={`px-3 py-1 rounded-full text-xs font-medium border transition-all ${v.active ? "bg-blue-50 border-blue-200 text-blue-700" : "bg-gray-50 border-gray-200 text-gray-400"}`}>
                        {v.active ? "✓ " : ""}{v.name}
                      </button>
                    ))}
                  </div>
                )}

                {/* Specs */}
                {designSpecs && (
                  <div className="border border-gray-200 rounded-2xl overflow-hidden">
                    <button onClick={() => setSpecsExpanded(!specsExpanded)} className="w-full flex items-center justify-between p-4 hover:bg-gray-50/50 transition-colors">
                      <div className="flex items-center gap-3">
                        <div className="h-8 w-8 rounded-full bg-blue-50 flex items-center justify-center"><Palette className="w-4 h-4 text-blue-600" /></div>
                        <div className="text-left"><div className="text-sm font-semibold flex items-center gap-2">整体设计规范 <Pencil className="w-3 h-3 text-gray-400" /></div>
                          <div className="text-[11px] text-gray-400">所有图片遵循的统一视觉标准</div></div>
                      </div>
                      {specsExpanded ? <ChevronUp className="w-4 h-4 text-gray-400" /> : <ChevronDown className="w-4 h-4 text-gray-400" />}
                    </button>
                    {specsExpanded && <div className="px-4 pb-4"><div className="bg-gray-50 rounded-xl p-4 text-xs text-gray-600 whitespace-pre-line leading-relaxed max-h-[400px] overflow-y-auto">{designSpecs}</div></div>}
                  </div>
                )}

                {/* Briefs */}
                {briefs.length > 0 && step === "planning" && (
                  <div className="space-y-2">
                    <div className="flex items-center gap-2 mb-3">
                      <div className="h-8 w-8 rounded-full bg-blue-50 flex items-center justify-center"><ImageIcon className="w-4 h-4 text-blue-600" /></div>
                      <div><div className="text-sm font-semibold">图片规划</div><div className="text-[11px] text-gray-400">共 {briefs.length} 张，点击可编辑</div></div>
                    </div>
                    {briefs.map((b, i) => (
                      <div key={i} className="border border-gray-200 rounded-xl overflow-hidden hover:border-gray-300 transition-colors">
                        <div className="p-3 flex items-start gap-3">
                          <div className="h-8 w-8 rounded-lg bg-gray-100 flex items-center justify-center flex-shrink-0"><span className="text-sm font-semibold text-gray-600">{i + 1}</span></div>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 mb-0.5">
                              <span className="text-sm font-semibold truncate">{b.title}</span>
                              <Pencil className="w-3 h-3 text-gray-400 cursor-pointer hover:text-blue-500" />
                              <Trash2 className="w-3 h-3 text-gray-400 cursor-pointer hover:text-red-500" />
                            </div>
                            <p className="text-xs text-gray-400 truncate">{b.description}</p>
                          </div>
                          <button onClick={() => setBriefs((p) => p.map((bb, j) => j === i ? { ...bb, expanded: !bb.expanded } : bb))} className="p-2 rounded-lg hover:bg-gray-100">
                            {b.expanded ? <ChevronUp className="w-4 h-4 text-gray-400" /> : <ChevronDown className="w-4 h-4 text-gray-400" />}
                          </button>
                        </div>
                        {b.expanded && <div className="px-3 pb-3"><div className="bg-gray-50 rounded-lg p-3 text-xs text-gray-600 whitespace-pre-line max-h-[300px] overflow-y-auto">{b.content}</div></div>}
                      </div>
                    ))}
                  </div>
                )}

                {/* Generated */}
                {generated.length > 0 && (
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-semibold">生成结果</span>
                        <Badge className="bg-white text-gray-600 border-gray-200">{generated.filter((g) => g.status === "done").length}/{generated.length}</Badge>
                      </div>
                      {step === "complete" && (
                        <button className="flex items-center gap-1.5 px-3 py-1.5 border border-gray-200 rounded-lg text-xs text-gray-600 hover:bg-gray-50">
                          <Download className="w-3.5 h-3.5" /> 下载全部
                        </button>
                      )}
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                      {generated.map((img) => (
                        <div key={img.id} className="group relative aspect-square rounded-xl border border-gray-200 overflow-hidden bg-gray-50 hover:border-gray-300 transition-all">
                          {img.status === "pending" ? (
                            <div className="flex flex-col items-center justify-center h-full">
                              <div className="h-8 w-8 rounded-lg bg-gray-100 flex items-center justify-center mb-2"><span className="text-xs font-medium text-gray-400">{img.id + 1}</span></div>
                              <span className="text-[11px] text-gray-300">等待中</span>
                            </div>
                          ) : img.status === "generating" ? (
                            <div className="flex flex-col items-center justify-center h-full">
                              <Loader2 className="w-6 h-6 animate-spin text-blue-400 mb-2" /><span className="text-[11px] text-blue-400">生成中...</span>
                            </div>
                          ) : img.status === "done" ? (
                            <>
                              <div className="w-full h-full bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center"><ImageIcon className="w-8 h-8 text-gray-300" /></div>
                              {img.score !== undefined && <div className="absolute top-2 right-2"><Badge className={scoreColor(img.score)}>{img.score}</Badge></div>}
                              {img.score !== undefined && img.score < 70 && <div className="absolute top-2 left-2"><div className="h-5 w-5 rounded-full bg-red-500/90 flex items-center justify-center"><AlertTriangle className="w-3 h-3 text-white" /></div></div>}
                              <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-all flex flex-col justify-end p-2.5">
                                <p className="text-[11px] text-white font-medium truncate mb-1">{img.title}</p>
                                {img.issue && <p className="text-[10px] text-red-300 truncate mb-1">{img.issue}</p>}
                                <div className="flex gap-1">
                                  <button className="flex items-center gap-1 h-7 px-2 text-[11px] text-white hover:bg-white/20 rounded-lg"><RefreshCw className="w-3 h-3" /> 重试</button>
                                  <button className="flex items-center h-7 px-2 text-white hover:bg-white/20 rounded-lg"><Download className="w-3 h-3" /></button>
                                </div>
                              </div>
                            </>
                          ) : (
                            <div className="flex flex-col items-center justify-center h-full">
                              <div className="h-8 w-8 rounded-full bg-red-50 flex items-center justify-center mb-2"><X className="w-4 h-4 text-red-400" /></div>
                              <span className="text-[11px] text-red-400">失败</span>
                              <button className="mt-1 text-[10px] text-blue-500 hover:underline">重试</button>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Status Bar */}
      {step !== "upload" && (
        <div className="fixed bottom-0 left-0 right-0 border-t border-gray-200 bg-white/90 backdrop-blur-sm px-6 py-2.5 flex items-center justify-between text-xs text-gray-500 z-50">
          <div className="flex items-center gap-4">
            {step === "generating" && (
              <>
                <span>生成进度</span>
                <div className="w-32 h-1.5 bg-gray-200 rounded-full overflow-hidden"><div className="h-full bg-blue-600 rounded-full transition-all" style={{ width: `${(generated.filter((g) => g.status === "done").length / (generated.length || 1)) * 100}%` }} /></div>
                <span>{generated.filter((g) => g.status === "done").length}/{generated.length}</span>
              </>
            )}
            {step === "complete" && <span className="text-emerald-600 font-medium flex items-center gap-1"><Check className="w-3.5 h-3.5" /> 完成</span>}
          </div>
          <span className="text-gray-400">{ratio} · {resolution} · {language === "none" ? "无文字" : language} · {model.includes("pro") ? "NB Pro" : model.includes("3.1") ? "NB 2" : "NB"}</span>
        </div>
      )}
    </div>
  );
}
