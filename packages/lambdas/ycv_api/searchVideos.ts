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

    if (statusCode1 !== 200) {
      console.error('Search videos failed with status:', statusCode1, videoIdsResponse);
      return InternalServerError(`Search videos failed: ${JSON.stringify(videoIdsResponse)}`, true);
    }

    let videoIds = videoIdsResponse.items.map((x: any)=>x.id.videoId).filter((x: any)=>![null, undefined].includes(x));

    if (videoIds.length === 0) {
      console.error('No valid video IDs found from search results');
      return BadRequest('No valid video IDs found from search results', true);
    }

    let [statusCode2, listVideoResuls] = await youtubeApiRepository.getVideoInformation('snippet', videoIds);

    if (statusCode2 !== 200) {
      console.error('Get video information failed with status:', statusCode2, listVideoResuls);
      return InternalServerError(`Get video information failed: ${JSON.stringify(listVideoResuls)}`, true);
    }

    return OK(listVideoResuls, true);
  }
  catch (e) {
    console.error(e);
    return InternalServerError(JSON.stringify(e), true);
  }
}