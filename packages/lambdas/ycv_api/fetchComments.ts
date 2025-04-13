import { YouTubeCommentThreadsParams } from "./types/types";
import { BadRequest, Forbidden, InternalServerError, NotFound, OK } from "./utils/apiResultUtils";
import youtubeApiRepository from "./repositories/youtubeApiRepository";

const validate = (parameters: YouTubeCommentThreadsParams) => {
  if (!parameters) {
    return 'parameters must be filled';
  }

  return null;
}

export async function main(event: any, context: any) {
  console.info('Processing message: ', event);

  const parameters: YouTubeCommentThreadsParams = event.queryStringParameters;

  const validationError = validate(parameters);

  if (validationError) {
    return BadRequest(validationError, true);
  }

  try {
    let [statusCode, videoCommentResults] = await youtubeApiRepository.fetchComments(parameters);

    if (statusCode === 403) {
      return Forbidden(videoCommentResults);
    }

    return OK(videoCommentResults, true);
  }
  catch (e) {
    console.error(e);
    return InternalServerError(JSON.stringify(e), true);
  }
}