import { Injectable } from "@angular/core";
import {
  HttpEvent,
  HttpInterceptor,
  HttpHandler,
  HttpRequest,
} from "@angular/common/http";
import { Observable } from "rxjs";
import { API_BASE_URL } from "./api.config";

@Injectable({ providedIn: "root" })
export class ApiInterceptor implements HttpInterceptor {
  intercept(
    req: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    const apiReq = req.clone({ url: `${API_BASE_URL}${req.url}` }); // The API_BASE_URL is now injected from the environment variable set during the Docker build process
    return next.handle(apiReq);
  }
} 