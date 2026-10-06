import { onRequestGet as __api_info_js_onRequestGet } from "E:\\网站项目\\smartimgkit\\functions\\api\\info.js"

export const routes = [
    {
      routePath: "/api/info",
      mountPath: "/api",
      method: "GET",
      middlewares: [],
      modules: [__api_info_js_onRequestGet],
    },
  ]