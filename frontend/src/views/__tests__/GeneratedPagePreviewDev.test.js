import { flushPromises, mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import GeneratedPagePreviewDev from '../GeneratedPagePreviewDev.vue'
import { getGeneratedPageArtifact } from '../../api/devGeneratedPageArtifact'

vi.mock('../../api/devGeneratedPageArtifact', () => ({
  getGeneratedPageArtifact: vi.fn(),
}))

const successArtifact = {
  version: '0.1',
  artifactType: 'generated-page',
  jobId: 'job_success',
  status: 'SUCCESS',
  htmlCode: '<main><h1>Hello preview</h1></main>',
  cssCode: '.lg-page { color: #111827; }',
  vueCode: '<template><main>Hello preview</main></template>',
  validation: {
    passed: true,
    errors: [],
    warnings: [
      {
        code: 'UNKNOWN_STYLE_FIELD',
        message: 'style 字段暂不支持',
        path: 'layout.children[0].style.unknown',
      },
    ],
  },
  unsupportedNodes: [
    {
      id: 'chart-1',
      type: 'chart',
      path: 'layout.children[1]',
    },
  ],
  source: {
    layoutHash: 'abc123',
    layoutVersion: '0.1',
    layoutSourceType: 'manual',
  },
  generator: {
    name: 'layout-static-generator',
    version: '0.1',
  },
  createdAt: '2026-05-08T10:00:00',
}

const failedArtifact = {
  ...successArtifact,
  jobId: 'job_failed',
  status: 'FAILED',
  htmlCode: '',
  cssCode: '',
  vueCode: '',
  validation: {
    passed: false,
    errors: [
      {
        code: 'LAYOUT_INVALID',
        message: 'layout 根节点缺失',
        path: 'layout',
      },
    ],
    warnings: [
      {
        code: 'IMAGE_SRC_MISSING',
        message: '图片缺少安全 src',
        path: 'layout.children[0]',
      },
    ],
  },
}

function mountPreview(jobId = 'job_success') {
  return mount(GeneratedPagePreviewDev, {
    props: { jobId },
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

describe('GeneratedPagePreviewDev', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('shows SUCCESS artifact with iframe, code, validation, and metadata', async () => {
    getGeneratedPageArtifact.mockResolvedValue(successArtifact)

    const wrapper = mountPreview('job_success')
    await flushPromises()

    expect(getGeneratedPageArtifact).toHaveBeenCalledWith('job_success')
    expect(wrapper.text()).toContain('job_success')
    expect(wrapper.text()).toContain('SUCCESS')
    expect(wrapper.text()).toContain('abc123')
    expect(wrapper.text()).toContain('layout-static-generator')
    expect(wrapper.text()).toContain('UNKNOWN_STYLE_FIELD')
    expect(wrapper.text()).toContain('style 字段暂不支持')
    expect(wrapper.text()).toContain('chart-1')
    expect(wrapper.text()).toContain('Hello preview')
    expect(wrapper.text()).toContain('.lg-page { color: #111827; }')
    expect(wrapper.text()).toContain('<template><main>Hello preview</main></template>')

    const iframe = wrapper.find('iframe')
    expect(iframe.exists()).toBe(true)
    expect(iframe.attributes('sandbox')).toBe('')
    expect(iframe.attributes('allow')).toBeUndefined()
    expect(iframe.html()).not.toContain('allow-scripts')
  })

  it('does not show iframe for FAILED artifact and shows validation errors', async () => {
    getGeneratedPageArtifact.mockResolvedValue(failedArtifact)

    const wrapper = mountPreview('job_failed')
    await flushPromises()

    expect(wrapper.text()).toContain('FAILED')
    expect(wrapper.text()).toContain('静态编译失败')
    expect(wrapper.text()).toContain('LAYOUT_INVALID')
    expect(wrapper.text()).toContain('layout 根节点缺失')
    expect(wrapper.text()).toContain('IMAGE_SRC_MISSING')
    expect(wrapper.text()).toContain('图片缺少安全 src')
    expect(wrapper.find('iframe').exists()).toBe(false)
  })

  it('shows empty state when artifact does not exist', async () => {
    getGeneratedPageArtifact.mockRejectedValue(
      new Error('generated-page artifact 不存在'),
    )

    const wrapper = mountPreview('job_missing')
    await flushPromises()

    expect(wrapper.text()).toContain('暂无 generated-page artifact')
    expect(wrapper.text()).toContain('generated-page artifact 不存在')
    expect(wrapper.find('iframe').exists()).toBe(false)
  })

  it('shows error state for unexpected request failures', async () => {
    getGeneratedPageArtifact.mockRejectedValue(new Error('网络请求失败'))

    const wrapper = mountPreview('job_error')
    await flushPromises()

    expect(wrapper.text()).toContain('查询失败')
    expect(wrapper.text()).toContain('网络请求失败')
    expect(wrapper.find('iframe').exists()).toBe(false)
  })
})
