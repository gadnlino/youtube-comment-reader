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
    let [statusCode1, videoIdsResponse] = await youtubeApiRepository.searchVideos({
      ...parameters,
      part: 'id'
    });

    let videoIds = videoIdsResponse.items.map((x: any)=>x.id.videoId).filter((x: any)=>![null, undefined].includes(x));

    let [statusCode2, listVideoResuls] = await youtubeApiRepository.listVideos('snippet', videoIds);

    return OK(listVideoResuls, true);
  }
  catch (e) {
    console.error(e);
    return InternalServerError(JSON.stringify(e), true);
  }
}