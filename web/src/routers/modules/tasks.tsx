import { LayoutWrap } from "../constant";
import { RouteObject } from "../interface";
import Tasks from "../../views/tasks";

const homeRouter: Array<RouteObject> = [
    {
        element: <LayoutWrap/>,
        children: [
            {
                path: "/home/tasks",
                element: <Tasks/>,
                meta: {
                    requiresAuth: true,
                    title: "扫描",
                    key: "/home/tasks"
                }
            }
        ]
    }
];

export default homeRouter