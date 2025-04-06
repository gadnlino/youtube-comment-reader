import { CommentsListParams } from "./types/types";
import { BadRequest, InternalServerError, OK } from "./utils/apiResultUtils";
import {fetchCommentReplies, fetchComments} from "./utils/youtubeApi"

const validate = (parameters: CommentsListParams) => {
  if(!parameters){
    return 'parameters must be filled';
  }

  return null;
}

export async function main(event: any, context: any) {
  console.info('Processing message: ', event);

  const parameters: CommentsListParams = event.queryStringParameters;

  const validationError = validate(parameters);

  if(validationError){
    return BadRequest(validationError, true);
  }

  let videoCommentResults : any | null = null;

  try {
   videoCommentResults = await fetchCommentReplies(parameters);
  }
  catch (e) {
    return InternalServerError(e, true);
  }

  return OK(videoCommentResults, true);
}