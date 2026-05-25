import { flushPromises, mount } from '@vue/test-utils'
import { beforeAll, beforeEach, describe, expect, it, vi } from 'vitest'
import ImageToLayoutDev from '../ImageToLayoutDev.vue'
import { generateImagePage, uploadImagePageSource } from '../../api/imageLayoutApi'

vi.mock('../../api/imageLayoutApi', () => ({
  uploadImagePageSource: vi.fn(),
  generateImagePage: vi.fn(),
}))

const uploadResult = {
  jobId: 'imgjob_real_001',
  fileName: 'demo.png',
  sourceUrl: '/api/image-page/jobs/imgjob_real_001/source',
}

const realAiResult = {
  status: 'SUCCESS',
  mode: 'real-ai',
  fallbackUsed: false,
  sourceType: 'REAL_AI',
  promptVersion: 'week10-v1',
  model: 'gpt-4.1-mini',
  durationMs: 1842,
  fallbackReason: '',
  warnings: [],
  errors: [],
  artifact: {
    reused: false,
    layoutFileName: 'layout.json',
    previewFileName: 'preview.html',
    metadataFileName: 'metadata.json',
  },
  validation: {
    ok: true,
    errors: [],
    warnings: [],
  },
  layoutJson: {
    version: '0.1',
    page: {
      name: '产品管理',
    },
    source: {
      type: 'screenshot',
    },
    tokens: {},
    layout: {
      type: 'page',
      children: [],
    },
    assets: [],
    responsive: {},
    assumptions: [],
    warnings: [],
  },
  previewHtml: '<!doctype html><html><head><style>.page{color:#111827;}</style></head><body><main class="page">REAL_AI</main></body></html>',
}

const fallbackResult = {
  ...realAiResult,
  status: 'SUCCESS',
  mode: 'fallback',
  fallbackUsed: true,
  sourceType: 'FALLBACK_RULE',
  fallbackReason: 'MODEL_NON_JSON_OUTPUT',
  warnings: [
    {
      code: 'FALLBACK_USED',
      message: '模型输出不可解析，已启用 fallback',
    },
  ],
  errors: [
    {
      code: 'MODEL_NON_JSON_OUTPUT',
      message: '模型未返回合法 JSON',
    },
  ],
  artifact: {
    reused: true,
    layoutFileName: 'layout.json',
    previewFileName: 'preview.html',
    metadataFileName: 'metadata.json',
  },
  previewHtml: '<!doctype html><html><body><main>FALLBACK</main></body></html>',
}

const failedResult = {
  ...realAiResult,
  status: 'FAILED',
  mode: 'real-ai',
  fallbackUsed: false,
  sourceType: 'REAL_AI',
  previewHtml: '',
  errors: [
    {
      code: 'PREVIEW_COMPILE_FAILED',
      message: 'preview 编译失败',
    },
  ],
  warnings: [
    {
      code: 'PARTIAL_LAYOUT',
      message: '部分节点已被跳过',
    },
  ],
  validation: {
    ok: false,
    errors: [
      {
        code: 'LAYOUT_INVALID',
        message: 'layout 根节点缺失必要字段',
      },
    ],
    warnings: [],
  },
  artifact: {
    reused: false,
    layoutFileName: 'layout.json',
    previewFileName: '',
    metadataFileName: 'metadata.json',
  },
}

function mountPage() {
  return mount(ImageToLayoutDev, {
    global: {
      stubs: {
        RouterLink: {
          props: ['to'],
          template: '<a :href="typeof to === `string` ? to : `#`"><slot /></a>',
        },
      },
    },
  })
}

async function selectFile(wrapper, file) {
  const input = wrapper.find('input[type="file"]')
  Object.defineProperty(input.element, 'files', {
    configurable: true,
    value: [file],
  })
  await input.trigger('change')
}

async function uploadSelectedFile(wrapper) {
  await wrapper.find('form').trigger('submit.prevent')
  await flushPromises()
}

async function generateForUploadedFile(wrapper) {
  await wrapper.find('button.secondary-button').trigger('click')
  await flushPromises()
}

beforeAll(() => {
  vi.stubGlobal('URL', {
    createObjectURL: vi.fn(() => 'blob:preview'),
    revokeObjectURL: vi.fn(),
  })
  Object.defineProperty(navigator, 'clipboard', {
    configurable: true,
    value: {
      writeText: vi.fn(),
    },
  })
})

describe('ImageToLayoutDev', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('shows REAL_AI state, promptVersion, artifact info, and secure iframe preview', async () => {
    uploadImagePageSource.mockResolvedValue(uploadResult)
    generateImagePage.mockResolvedValue(realAiResult)

    const wrapper = mountPage()
    const file = new File(['fake-image'], 'demo.png', { type: 'image/png' })

    await selectFile(wrapper, file)
    await uploadSelectedFile(wrapper)
    await generateForUploadedFile(wrapper)

    expect(uploadImagePageSource).toHaveBeenCalledTimes(1)
    expect(uploadImagePageSource).toHaveBeenCalledWith(file)
    expect(generateImagePage).toHaveBeenCalledWith('imgjob_real_001')

    expect(wrapper.text()).toContain('REAL_AI 成功')
    expect(wrapper.text()).toContain('REAL_AI')
    expect(wrapper.text()).toContain('week10-v1')
    expect(wrapper.text()).toContain('gpt-4.1-mini')
    expect(wrapper.text()).toContain('1842 ms')
    expect(wrapper.text()).toContain('layout.json')
    expect(wrapper.text()).toContain('preview.html')
    expect(wrapper.text()).toContain('metadata.json')
    expect(wrapper.text()).toContain('artifact.reused')
    expect(wrapper.text()).toContain('false')
    expect(wrapper.text()).toContain('/api/image-page/jobs/imgjob_real_001/source')
    expect(wrapper.text()).toContain('原图 / 生成预览')
    expect(wrapper.text()).toContain('上传原图')
    expect(wrapper.text()).toContain('生成预览')
    expect(wrapper.text()).toContain('交付操作')
    expect(wrapper.text()).toContain('复制 HTML')
    expect(wrapper.text()).toContain('复制 CSS')
    expect(wrapper.text()).toContain('复制完整 HTML')
    expect(wrapper.text()).toContain('下载 HTML')
    expect(wrapper.text()).toContain('调试详情')
    expect(wrapper.find('.image-compare-grid').exists()).toBe(true)
    expect(wrapper.find('.compare-image-frame img').attributes('src')).toBe(uploadResult.sourceUrl)

    const deliveryButtons = wrapper.findAll('.delivery-action-grid button')
    expect(deliveryButtons).toHaveLength(4)
    expect(deliveryButtons[0].attributes('disabled')).toBeUndefined()
    expect(deliveryButtons[1].attributes('disabled')).toBeUndefined()
    expect(deliveryButtons[2].attributes('disabled')).toBeUndefined()
    expect(deliveryButtons[3].attributes('disabled')).toBeUndefined()

    const iframe = wrapper.find('iframe')
    expect(iframe.exists()).toBe(true)
    expect(iframe.attributes('sandbox')).toBe('')
    expect(iframe.attributes('allow')).toBeUndefined()
    expect(iframe.html()).not.toContain('allow-scripts')
  })

  it('copies HTML, CSS, and full HTML document from previewHtml', async () => {
    uploadImagePageSource.mockResolvedValue(uploadResult)
    generateImagePage.mockResolvedValue(realAiResult)
    navigator.clipboard.writeText.mockResolvedValue()

    const wrapper = mountPage()
    const file = new File(['fake-image'], 'demo.png', { type: 'image/png' })

    await selectFile(wrapper, file)
    await uploadSelectedFile(wrapper)
    await generateForUploadedFile(wrapper)

    const deliveryButtons = wrapper.findAll('.delivery-action-grid button')

    await deliveryButtons[0].trigger('click')
    await flushPromises()
    expect(navigator.clipboard.writeText).toHaveBeenLastCalledWith(
      expect.stringContaining('<main class="page">REAL_AI</main>'),
    )
    expect(navigator.clipboard.writeText.mock.calls.at(-1)[0]).not.toContain('<style>')
    expect(wrapper.text()).toContain('HTML 已复制')

    await deliveryButtons[1].trigger('click')
    await flushPromises()
    expect(navigator.clipboard.writeText).toHaveBeenLastCalledWith('.page{color:#111827;}')
    expect(wrapper.text()).toContain('CSS 已复制')

    await deliveryButtons[2].trigger('click')
    await flushPromises()
    expect(navigator.clipboard.writeText).toHaveBeenLastCalledWith(realAiResult.previewHtml)
    expect(wrapper.text()).toContain('完整 HTML 已复制')
  })

  it('downloads full HTML document as a single html file', async () => {
    uploadImagePageSource.mockResolvedValue(uploadResult)
    generateImagePage.mockResolvedValue(realAiResult)
    const clickSpy = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {})

    const wrapper = mountPage()
    const file = new File(['fake-image'], 'demo.png', { type: 'image/png' })

    await selectFile(wrapper, file)
    await uploadSelectedFile(wrapper)
    await generateForUploadedFile(wrapper)

    await wrapper.findAll('.delivery-action-grid button')[3].trigger('click')
    await flushPromises()

    const blob = URL.createObjectURL.mock.calls.at(-1)[0]
    expect(blob).toBeInstanceOf(Blob)
    expect(blob.type).toBe('text/html;charset=utf-8')
    expect(clickSpy).toHaveBeenCalledTimes(1)
    expect(URL.revokeObjectURL).toHaveBeenCalledWith('blob:preview')
    expect(wrapper.text()).toContain('完整 HTML 已开始下载')

    clickSpy.mockRestore()
  })

  it('shows readable copy failure message without changing generated result', async () => {
    uploadImagePageSource.mockResolvedValue(uploadResult)
    generateImagePage.mockResolvedValue(realAiResult)
    navigator.clipboard.writeText.mockRejectedValue(new Error('clipboard denied'))

    const wrapper = mountPage()
    const file = new File(['fake-image'], 'demo.png', { type: 'image/png' })

    await selectFile(wrapper, file)
    await uploadSelectedFile(wrapper)
    await generateForUploadedFile(wrapper)

    await wrapper.findAll('.delivery-action-grid button')[0].trigger('click')
    await flushPromises()

    expect(wrapper.text()).toContain('HTML 复制失败，请检查浏览器剪贴板权限')
    expect(wrapper.text()).toContain('REAL_AI 成功：可交付')
    expect(wrapper.text()).toContain('当前结果由真实 AI 直接生成，未触发 fallback。')
    expect(wrapper.text()).toContain('使用下方按钮复制 HTML / CSS，或下载完整 HTML。')
    expect(wrapper.find('iframe').attributes('sandbox')).toBe('')
  })

  it('shows MVP result flow before debug details', async () => {
    uploadImagePageSource.mockResolvedValue(uploadResult)
    generateImagePage.mockResolvedValue(realAiResult)

    const wrapper = mountPage()
    const file = new File(['fake-image'], 'demo.png', { type: 'image/png' })

    await selectFile(wrapper, file)
    await uploadSelectedFile(wrapper)
    await generateForUploadedFile(wrapper)

    const summaryText = wrapper.text()
    expect(summaryText).toContain('生成状态')
    expect(summaryText).toContain('下一步')
    expect(summaryText).toContain('原图 / 生成预览')
    expect(summaryText).toContain('交付操作')
    expect(summaryText).toContain('调试详情')
    expect(summaryText.indexOf('生成状态')).toBeLessThan(summaryText.indexOf('原图 / 生成预览'))
    expect(summaryText.indexOf('原图 / 生成预览')).toBeLessThan(summaryText.indexOf('交付操作'))
    expect(summaryText.indexOf('交付操作')).toBeLessThan(summaryText.indexOf('调试详情'))
    expect(summaryText).toContain('model')
    expect(summaryText).toContain('gpt-4.1-mini')
    expect(summaryText).toContain('promptVersion')
    expect(summaryText).toContain('week10-v1')
    expect(summaryText).toContain('sourceType')
    expect(summaryText).toContain('REAL_AI')
    expect(summaryText).toContain('artifact.reused')
  })

  it('shows FALLBACK state and fallbackReason with visible warnings and errors', async () => {
    uploadImagePageSource.mockResolvedValue(uploadResult)
    generateImagePage.mockResolvedValue(fallbackResult)

    const wrapper = mountPage()
    const file = new File(['fake-image'], 'demo.png', { type: 'image/png' })

    await selectFile(wrapper, file)
    await uploadSelectedFile(wrapper)
    await generateForUploadedFile(wrapper)

    expect(wrapper.text()).toContain('FALLBACK：保底结果可预览')
    expect(wrapper.text()).toContain('当前结果来自 fallback 保底规则')
    expect(wrapper.text()).toContain('不要当作真实 AI 命中结果')
    expect(wrapper.text()).toContain('重新生成或检查输入图')
    expect(wrapper.text()).toContain('MODEL_NON_JSON_OUTPUT')
    expect(wrapper.text()).toContain('模型未返回合法 JSON')
    expect(wrapper.text()).toContain('模型输出不可解析，已启用 fallback')
    expect(wrapper.text()).toContain('gpt-4.1-mini')
    expect(wrapper.text()).toContain('1842 ms')
    expect(wrapper.text()).toContain('true')
    expect(wrapper.text()).toContain('FALLBACK_RULE')
    expect(wrapper.text()).toContain('artifact.reused')
    expect(wrapper.text()).toContain('true')

    const iframe = wrapper.find('iframe')
    expect(iframe.exists()).toBe(true)
    expect(iframe.attributes('sandbox')).toBe('')
    expect(iframe.attributes('allow')).toBeUndefined()
  })

  it('shows FAILED state, errors, warnings, and no iframe preview', async () => {
    uploadImagePageSource.mockResolvedValue(uploadResult)
    generateImagePage.mockResolvedValue(failedResult)

    const wrapper = mountPage()
    const file = new File(['fake-image'], 'demo.png', { type: 'image/png' })

    await selectFile(wrapper, file)
    await uploadSelectedFile(wrapper)
    await generateForUploadedFile(wrapper)

    expect(wrapper.text()).toContain('FAILED：暂无可交付结果')
    expect(wrapper.text()).toContain('当前生成失败，暂时没有可预览或可下载的页面。')
    expect(wrapper.text()).toContain('查看 errors / validation.errors 定位失败原因。')
    expect(wrapper.text()).toContain('修正输入图片或稍后重试。')
    expect(wrapper.text()).toContain('preview 编译失败')
    expect(wrapper.text()).toContain('PARTIAL_LAYOUT')
    expect(wrapper.text()).toContain('LAYOUT_INVALID')
    expect(wrapper.text()).toContain('当前结果为 FAILED，不展示 iframe 预览。')
    expect(wrapper.find('.image-compare-grid').exists()).toBe(true)
    expect(wrapper.text()).toContain('暂无 iframe')
    expect(wrapper.text()).toContain('生成成功且存在 previewHtml 后，这里会展示安全 iframe 预览。')
    expect(wrapper.find('iframe').exists()).toBe(false)
  })

  it('handles missing optional model and durationMs metadata without breaking artifact.reused', async () => {
    uploadImagePageSource.mockResolvedValue(uploadResult)
    generateImagePage.mockResolvedValue({
      ...realAiResult,
      model: undefined,
      durationMs: undefined,
      artifact: {
        ...realAiResult.artifact,
        reused: false,
      },
    })

    const wrapper = mountPage()
    const file = new File(['fake-image'], 'demo.png', { type: 'image/png' })

    await selectFile(wrapper, file)
    await uploadSelectedFile(wrapper)
    await generateForUploadedFile(wrapper)

    expect(wrapper.text()).toContain('REAL_AI 成功：可交付')
    expect(wrapper.text()).toContain('model')
    expect(wrapper.text()).toContain('durationMs')
    expect(wrapper.text()).toContain('artifact.reused')
    expect(wrapper.text()).toContain('false')
    expect(wrapper.find('iframe').attributes('sandbox')).toBe('')
  })

  it('shows TIMEOUT state when generate request times out', async () => {
    uploadImagePageSource.mockResolvedValue(uploadResult)
    generateImagePage.mockRejectedValue(new Error('Worker timeout after 120 seconds'))

    const wrapper = mountPage()
    const file = new File(['fake-image'], 'demo.png', { type: 'image/png' })

    await selectFile(wrapper, file)
    await uploadSelectedFile(wrapper)
    await generateForUploadedFile(wrapper)

    expect(wrapper.text()).toContain('生成超时')
    expect(wrapper.text()).toContain('Worker timeout after 120 seconds')
    expect(wrapper.text()).toContain('TIMEOUT：生成超时')
    expect(wrapper.text()).toContain('稍后重试，或换一张内容更少、更清晰的截图。')
    expect(wrapper.find('iframe').exists()).toBe(false)
  })

  it('does not upload when no image is selected', async () => {
    const wrapper = mountPage()

    await uploadSelectedFile(wrapper)

    expect(uploadImagePageSource).not.toHaveBeenCalled()
    expect(generateImagePage).not.toHaveBeenCalled()
    expect(wrapper.text()).toContain('请先选择一张本地图片')
    expect(wrapper.find('iframe').exists()).toBe(false)
  })
})
