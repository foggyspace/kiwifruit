export interface MetaProps {
    keepAlive?: boolean;
    requestsAuth?: boolean;
    title?: string;
    key?: string;
}

export interface RouteObject {
    caseSensitive?: boolean;
    children?: RouteObject[];
    element?: React.ReactNode;
    index?: boolean;
    path?: string;
    meta?: MetaProps;
    isLink?: string;
}

