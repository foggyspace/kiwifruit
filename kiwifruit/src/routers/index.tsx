import { Navigate, useRoutes } from "react-router-dom";
import { RouteObject } from "./interface";

import Login from "../views/login/";
import LayoutIndex from "../layouts";
import lazyLoad from "./utils/lazyLoad";


export const rootRouter: RouteObject[] = [
    {
        path: "/",
        element: <Navigate to="/login">
    },
    {
        path: "/login",
        element: <Login/>,
        meta: {
            requestsAuth: false,
            title: "用户登录",
            key: "login"
        },
    },
    {
        path: "/home",
        element: <LayoutIndex/>
        children: [
            {
                path: "/task",
                element: <Login/>
            }
        ]
    },
    {
        path: "*",
        element: <Navigate to="/404" />
    },
    {
        path: "/403",
        element: lazyLoad(React.lazy(() => import("@/components/ErrorMessage/403"))),
        meta: {
            requestsAuth: false,
            title: "403页面",
            key: "500"
        }
    },
    {
        path: "/500",
        element: lazyLoad(React.lazy(() => import("@/components/ErrorMessage/500"))),
        meta: {
            requestsAuth: false,
            title: "500页面",
            key: "500"
        }
    }
];

const Router = () => {
    const routes = useRoutes(rootRouter);
    return routes;
};

export default Router;

