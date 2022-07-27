import {defineConfig} from 'vitepress'

export default defineConfig({
    lang: "zh-CN",
    base: "/scrapy-demo/",
    description: "Scrapy 学习",
    lastUpdated: true,
    themeConfig: {
        logo: "https://docs.python.org/zh-cn/3/_static/py.svg",
        siteTitle: "Scrapy",
        outlineTitle: "章节导航",
        lastUpdatedText: "最后更新时间",
        editLink: {
            pattern: "https://github.com/curder/scrapy-demo/edit/master/docs/:path",
            text: '编辑它'
        },
        socialLinks: [
            {icon: 'github', link: 'https://github.com/curder/scrapy-demo'}
        ],
        nav: nav(),
        sidebar: {
            "/guide": sidebarGuide(),
        }
    }
});

function nav() {
    return [
        {text: 'Guide', link: '/guide/basic', activeMatch: '/guide/'},
    ];
}

function sidebarGuide() {
    return [
        {
            text: "基础",
            collapsible: true,
            collapsed: false,
            items: [
                {text: "概念和工作流程", link: "/guide/basic"},
            ]
        },
    ];
}