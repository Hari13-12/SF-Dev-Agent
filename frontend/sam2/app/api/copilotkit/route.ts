import {
  CopilotRuntime,
//   OpenAIAdapter,
GoogleGenerativeAIAdapter,
  copilotRuntimeNextJSAppRouterEndpoint
} from "@copilotkit/runtime";

import { NextRequest } from "next/server";
import { LangGraphHttpAgent } from "@copilotkit/runtime/langgraph";



const serviceAdapter = new GoogleGenerativeAIAdapter({
  apiKey: "AIzaSyC7P5I83jQ9TwJRdfQOi3C0dRrzncuTU4E",
  model: "models/gemini-2.5-flash",
});
 const runtime = new CopilotRuntime({
//   agents: {
//     sample_agent: new LangGraphHttpAgent({
//       url:  process.env.LANGGRAPH_DEPLOYMENT_URL || "http://localhost:8000",
//     }),
//   }
agents: {
  default: new LangGraphHttpAgent({  // Remap to "default"
    url: process.env.LANGGRAPH_DEPLOYMENT_URL || "http://localhost:8000",
  }),
}

});


export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};