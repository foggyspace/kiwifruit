import { LayoutWrap } from "../constant";
import { RouteObject } from "../interface";
import Home from "../../views/home";

const homeRouter: Array<RouteObject> = [
    {
        element: <LayoutWrap/>,
        children: [
            {
                path: "/home/index",
                element: <Home/>,
                meta: {
                    requiresAuth: true,
                    title: "首页",
                    key: "/home/index"
                }
            }
        ]
    }
];

export default homeRouter