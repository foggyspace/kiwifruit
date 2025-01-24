import { LayoutWrap } from "../constant";
import { RouteObject } from "../interface";
import VulnerabilityList from "../../views/vulnerabilities";

const homeRouter: Array<RouteObject> = [
    {
        element: <LayoutWrap/>,
        children: [
            {
                path: "/home/vulns",
                element: <VulnerabilityList/>,
                meta: {
                    requiresAuth: true,
                    title: "漏洞",
                    key: "/home/vulns"
                }
            }
        ]
    }
];

export default homeRouter