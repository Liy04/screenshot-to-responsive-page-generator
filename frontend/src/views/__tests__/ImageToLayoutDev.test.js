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
  previewHtml: '<!doctype html><html><body><main>REAL_AI</main></body></html>',
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
    expect(wrapper.text()).toContain('layout.json')
    expect(wrapper.text()).toContain('preview.html')
    expect(wrapper.text()).toContain('metadata.json')
    expect(wrapper.text()).toContain('false')
    expect(wrapper.text()).toContain('/api/image-page/jobs/imgjob_real_001/source')

    const iframe = wrapper.find('iframe')
    expect(iframe.exists()).toBe(true)
    expect(iframe.attributes('sandbox')).toBe('')
    expect(iframe.attributes('allow')).toBeUndefined()
    expect(iframe.html()).not.toContain('allow-scripts')
  })

  it('shows FALLBACK state and fallbackReason with visible warnings and errors', async () => {
    uploadImagePageSource.mockResolvedValue(uploadResult)
    generateImagePage.mockResolvedValue(fallbackResult)

    const wrapper = mountPage()
    const file = new File(['fake-image'], 'demo.png', { type: 'image/png' })

    await selectFile(wrapper, file)
    await uploadSelectedFile(wrapper)
    await generateForUploadedFile(wrapper)

    expect(wrapper.text()).toContain('FALLBACK')
    expect(wrapper.text()).toContain('MODEL_NON_JSON_OUTPUT')
    expect(wrapper.text()).toContain('模型未返回合法 JSON')
    expect(wrapper.text()).toContain('模型输出不可解析，已启用 fallback')
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

    expect(wrapper.text()).toContain('FAILED')
    expect(wrapper.text()).toContain('preview 编译失败')
    expect(wrapper.text()).toContain('PARTIAL_LAYOUT')
    expect(wrapper.text()).toContain('LAYOUT_INVALID')
    expect(wrapper.text()).toContain('当前结果为 FAILED，不展示 iframe 预览。')
    expect(wrapper.find('iframe').exists()).toBe(false)
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
