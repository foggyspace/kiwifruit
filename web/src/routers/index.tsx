import {RouteObject} from "./interface";
import {Navigate, useRoutes} from "react-router-dom";
import Login from "../views/login";
import NotFound from "../components/ErrorMessage/404";

interface ModuleType {
    [key: string]: RouteObject[];
}

const metaRouters: Record<string, ModuleType> = import.meta.glob("./modules/*.tsx", {eager: true});

export const routerArray: RouteObject[] = [];

Object.keys(metaRouters).forEach(item => {
    Object.keys(metaRouters[item]).forEach((key: string) => {
        routerArray.push(...metaRouters[item][key]);
    });
});

export const rootRouter: RouteObject[] = [
    {
        path: "/",
        element: <Navigate to="/login"/>
    },
    {
        path: "/login",
        element: <Login/>,
        meta: {
            requiresAuth: false,
            title: "登录",
            key: "login"
        }
    },
    ...routerArray,
    {
        path: "*",
        element: <NotFound />
    }
]

const Router = () => {
    const routes = useRoutes(rootRouter as import('react-router').RouteObject[])
    return routes
}

export default Router