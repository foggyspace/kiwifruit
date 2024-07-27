import { Navigate, useRoutes } from "react-router-dom";
import { RouteObject } from "./interface";

import Login from "../views/login/";
import LayoutIndex from "../layouts";


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
    }
];

const Router = () => {
    const routes = useRoutes(rootRouter);
    return routes;
};

export default Router;

