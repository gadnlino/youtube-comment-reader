import { YouTubeSearchParams } from "./types/types";
import { BadRequest, InternalServerError, NotFound, OK } from "./utils/apiResultUtils";
import youtubeApiRepository from "./repositories/youtubeApiRepository";

const validate = (parameters: YouTubeSearchParams) => {
  if (!parameters) {
    return 'parameters must be filled';
  }

  return null;
}

export async function main(event: any, context: any) {
  console.log('Processing message: ', event);

  let parameters: YouTubeSearchParams = event.queryStringParameters;

  const validationError = validate(parameters);

  if (validationError) {
    return BadRequest(validationError, true);
  }

  try {
    let [statusCode, searchVideoResults] = await youtubeApiRepository.searchVideos(parameters);

    return OK(searchVideoResults, true);
  }
  catch (e) {
    console.error(e);
    return InternalServerError(JSON.stringify(e), true);
  }
}