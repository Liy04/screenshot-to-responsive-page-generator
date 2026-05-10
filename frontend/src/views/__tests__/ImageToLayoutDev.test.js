import { flushPromises, mount } from '@vue/test-utils'
import { beforeAll, beforeEach, describe, expect, it, vi } from 'vitest'
import ImageToLayoutDev from '../ImageToLayoutDev.vue'
import { createImagePageJob } from '../../api/imageLayoutApi'

vi.mock('../../api/imageLayoutApi', () => ({
  createImagePageJob: vi.fn(),
}))

const landingSuccessResult = {
  jobId: 'img-page-landing-001',
  status: 'SUCCESS',
  sourceType: 'IMAGE_TEMPLATE_MOCK',
  imageName: 'demo.png',
  templateKey: 'landing-basic',
  layoutArtifact: {
    status: 'SUCCESS',
    layoutJson: {
      version: '0.1',
      page: {
        title: 'Landing Page',
      },
      source: {
        type: 'manual',
      },
      tokens: {},
      layout: {
        type: 'page',
        children: [
          {
            type: 'section',
            children: [
              {
                type: 'text',
                role: 'heading',
                content: 'Landing Hero',
              },
            ],
          },
        ],
      },
      assets: [],
      responsive: {},
      assumptions: [],
      warnings: [],
    },
  },
  generatedPageArtifact: {
    status: 'SUCCESS',
    htmlCode: '<main><section><h1>Landing Hero</h1></section></main>',
    cssCode: '.hero { color: #111827; }',
    vueCode: '<template><main>Landing Hero</main></template>',
  },
  errors: [],
  warnings: [],
}

const cardListSuccessResult = {
  ...landingSuccessResult,
  jobId: 'img-page-card-list-001',
  imageName: 'cards.png',
  templateKey: 'card-list',
  layoutArtifact: {
    ...landingSuccessResult.layoutArtifact,
    layoutJson: {
      ...landingSuccessResult.layoutArtifact.layoutJson,
      page: {
        title: 'Card List',
      },
      layout: {
        type: 'page',
        children: [
          {
            type: 'list',
            children: [
              {
                type: 'listItem',
                children: [
                  {
                    type: 'text',
                    content: 'Card Item 1',
                  },
                ],
              },
            ],
          },
        ],
      },
    },
  },
  generatedPageArtifact: {
    status: 'SUCCESS',
    htmlCode: '<main><ul><li>Card Item 1</li></ul></main>',
    cssCode: '.card-list { display: grid; gap: 16px; }',
    vueCode: '<template><main>Card List</main></template>',
  },
}

const invalidLayoutResult = {
  jobId: 'img-page-invalid-001',
  status: 'FAILED',
  sourceType: 'IMAGE_TEMPLATE_MOCK',
  imageName: 'invalid.png',
  templateKey: 'invalid-layout',
  layoutArtifact: {
    status: 'FAILED',
    layoutJson: {
      version: '0.1',
      page: {},
      source: {},
      tokens: {},
      layout: {},
      assets: [],
      responsive: {},
      assumptions: [],
      warnings: [],
    },
  },
  generatedPageArtifact: null,
  errors: [
    {
      code: 'LAYOUT_INVALID',
      message: 'layout 根节点缺失必要字段',
      path: 'layout',
    },
  ],
  warnings: [
    {
      code: 'TEMPLATE_DEGRADED',
      message: '模板仅返回失败调试信息',
      path: 'layout',
    },
  ],
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

async function submitForm(wrapper) {
  await wrapper.find('form').trigger('submit.prevent')
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

  it('submits landing-basic with imageName and shows SUCCESS artifact with secure iframe', async () => {
    createImagePageJob.mockResolvedValue(landingSuccessResult)

    const wrapper = mountPage()
    const file = new File(['fake-image'], 'demo.png', { type: 'image/png' })

    await selectFile(wrapper, file)
    await wrapper.find('#template-key-select').setValue('landing-basic')
    await submitForm(wrapper)

    expect(createImagePageJob).toHaveBeenCalledWith({
      imageName: 'demo.png',
      templateKey: 'landing-basic',
    })

    const requestPayload = createImagePageJob.mock.calls[0][0]
    expect(requestPayload).not.toBe(file)
    expect(requestPayload.file).toBeUndefined()
    expect(requestPayload.base64).toBeUndefined()
    expect(requestPayload.formData).toBeUndefined()
    expect(requestPayload.imageName).toBe('demo.png')
    expect(requestPayload.templateKey).toBe('landing-basic')

    expect(wrapper.text()).toContain('img-page-landing-001')
    expect(wrapper.text()).toContain('SUCCESS')
    expect(wrapper.text()).toContain('IMAGE_TEMPLATE_MOCK')
    expect(wrapper.text()).toContain('Landing Page')
    expect(wrapper.text()).toContain('generatedPageArtifact')
    expect(wrapper.text()).toContain('Landing Hero')
    expect(wrapper.text()).toContain('.hero { color: #111827; }')
    expect(wrapper.text()).toContain('<template><main>Landing Hero</main></template>')

    const iframe = wrapper.find('iframe')
    expect(iframe.exists()).toBe(true)
    expect(iframe.attributes('sandbox')).toBe('')
    expect(iframe.attributes('allow')).toBeUndefined()
    expect(iframe.html()).not.toContain('allow-scripts')
  })

  it('shows generatedPageArtifact for card-list and keeps iframe sandbox safe', async () => {
    createImagePageJob.mockResolvedValue(cardListSuccessResult)

    const wrapper = mountPage()
    const file = new File(['fake-image'], 'cards.png', { type: 'image/png' })

    await selectFile(wrapper, file)
    await wrapper.find('#template-key-select').setValue('card-list')
    await submitForm(wrapper)

    expect(createImagePageJob).toHaveBeenCalledWith({
      imageName: 'cards.png',
      templateKey: 'card-list',
    })
    expect(wrapper.text()).toContain('img-page-card-list-001')
    expect(wrapper.text()).toContain('Card List')
    expect(wrapper.text()).toContain('Card Item 1')
    expect(wrapper.text()).toContain('.card-list { display: grid; gap: 16px; }')
    expect(wrapper.text()).toContain('<template><main>Card List</main></template>')

    const iframe = wrapper.find('iframe')
    expect(iframe.exists()).toBe(true)
    expect(iframe.attributes('sandbox')).toBe('')
    expect(iframe.attributes('allow')).toBeUndefined()
    expect(iframe.html()).not.toContain('allow-scripts')
  })

  it('shows FAILED state for invalid-layout and does not render iframe', async () => {
    createImagePageJob.mockResolvedValue(invalidLayoutResult)

    const wrapper = mountPage()
    const file = new File(['fake-image'], 'invalid.png', { type: 'image/png' })

    await selectFile(wrapper, file)
    await wrapper.find('#template-key-select').setValue('invalid-layout')
    await submitForm(wrapper)

    expect(createImagePageJob).toHaveBeenCalledWith({
      imageName: 'invalid.png',
      templateKey: 'invalid-layout',
    })
    expect(wrapper.text()).toContain('FAILED')
    expect(wrapper.text()).toContain('LAYOUT_INVALID')
    expect(wrapper.text()).toContain('layout 根节点缺失必要字段')
    expect(wrapper.text()).toContain('TEMPLATE_DEGRADED')
    expect(wrapper.text()).toContain('当前结果为 FAILED 或缺少 generatedPageArtifact，不展示 iframe 预览。')
    expect(wrapper.find('iframe').exists()).toBe(false)
  })

  it('shows error state when createImagePageJob rejects', async () => {
    createImagePageJob.mockRejectedValue(new Error('Unknown templateKey'))

    const wrapper = mountPage()
    const file = new File(['fake-image'], 'demo.png', { type: 'image/png' })

    await selectFile(wrapper, file)
    await submitForm(wrapper)

    expect(wrapper.text()).toContain('请求失败')
    expect(wrapper.text()).toContain('Unknown templateKey')
    expect(wrapper.find('iframe').exists()).toBe(false)
  })

  it('does not submit when no image is selected', async () => {
    const wrapper = mountPage()

    await submitForm(wrapper)

    expect(createImagePageJob).not.toHaveBeenCalled()
    expect(wrapper.text()).toContain('请先选择一张本地图片')
    expect(wrapper.find('iframe').exists()).toBe(false)
  })
})
