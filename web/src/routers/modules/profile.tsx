import { LayoutWrap } from "../constant";
import { RouteObject } from "../interface";
import Profile from "../../views/profile";

const homeRouter: Array<RouteObject> = [
    {
        element: <LayoutWrap/>,
        children: [
            {
                path: "/home/profile",
                element: <Profile/>,
                meta: {
                    requiresAuth: true,
                    title: "用户详情",
                    key: "/home/profile"
                }
            }
        ]
    }
];

export default homeRouter