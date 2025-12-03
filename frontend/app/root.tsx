import { Outlet } from "react-router";
import "./app.css";
import {authMiddleware} from "./middleware";
export const clientMiddleware: Route.clientMiddlewareFunction[] = [authMiddleware];

export default function App() {
  return (
    <html>
      <head>
        <title>Jobify</title>
      </head>
      <body>
        <Outlet></Outlet>
      </body>
    </html>
  )
}

