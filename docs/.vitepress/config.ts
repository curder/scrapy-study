import {defineConfig} from 'vitepress'

export default defineConfig({
    lang: "zh-CN",
    title: "Scrapy",
    base: "/scrapy-study/",
    description: "Scrapy 学习",
    lastUpdated: true,
    themeConfig: {
        logo: "https://scrapy.org/img/scrapylogo.png",
        siteTitle: "",
        outlineTitle: "章节导航",
        lastUpdatedText: "最后更新时间",
        editLink: {
            pattern: "https://github.com/curder/scrapy-study/edit/master/docs/:path",
            text: '编辑它'
        },
        socialLinks: [
            {icon: 'github', link: 'https://github.com/curder/scrapy-study'}
        ],
        nav: nav(),
        sidebar: {
            "/guide": sidebarGuide(),
        }
    }
});

function nav() {
    return [
        {text: 'Guide', link: '/guide/getting-started', activeMatch: '/guide/'},
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
                {text: "入门使用", link: "/guide/getting-started"},
                {text: "数据建模", link: "/guide/data-modeling"},
                {text: "构造分页请求", link: "/guide/construct-paging-request"},
                {text: "模拟登录", link: "/guide/simulate-login"},
                {text: "管道 Pipelines", link: "/guide/pipelines"},
                {text: "链接提取器", link: "/guide/link-extractors"},
                {text: "中间件", link: "/guide/middlewares"},
            ]
        },
        {
            text: "其他组件",
            collapsible: true,
            collapsed: false,
            items: [
                {text: "Scrapy Redis分布式爬虫", link: "/guide/components/scrapy-redis"},
            ]
        }
    ];
}