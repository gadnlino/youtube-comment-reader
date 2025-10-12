/**
 * Test script for the updated sentiment analysis API
 * 
 * This script tests the new Lambda-based sentiment analysis API
 * to ensure it works correctly with the TF-IDF classifier.
 */

import sentimentAnalysisApi from './utils/sentimentAnalysisApi';

async function testSentimentAnalysis() {
    console.log('🧪 Testing sentiment analysis API with Lambda function...');
    
    try {
        // Test data
        const testComments = [
            {
                id: 'test-1',
                text: 'This video is absolutely amazing! I love it!',
                videoTitle: 'Great Tutorial'
            },
            {
                id: 'test-2', 
                text: 'I hate this video, it was terrible.',
                videoTitle: 'Bad Example'
            },
            {
                id: 'test-3',
                text: 'It was okay, nothing special.',
                videoTitle: 'Average Content'
            }
        ];

        console.log('📝 Test comments:');
        testComments.forEach(comment => {
            console.log(`  - "${comment.text}" (Video: ${comment.videoTitle})`);
        });

        console.log('\n🔄 Calling sentiment analysis API via Lambda Function URL...');
        
        const startTime = Date.now();
        const results = await sentimentAnalysisApi.analyzeSentiments({
            comments: testComments,
            model_name: 'tfidf'
        });
        const endTime = Date.now();

        console.log(`✅ Sentiment analysis completed in ${endTime - startTime}ms`);
        console.log('\n📊 Results:');
        
        results.forEach((result, index) => {
            console.log(`  ${index + 1}. "${result.text}"`);
            console.log(`     Sentiment: ${result.sentiment}`);
            console.log(`     Score: ${result.score?.toFixed(3)}`);
            console.log(`     Label: ${result.label}`);
            console.log('');
        });

        console.log('🎉 Sentiment analysis API test completed successfully!');
        
    } catch (error) {
        console.error('❌ Error testing sentiment analysis API:', error);
        throw error;
    }
}

// Run the test if this file is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
    testSentimentAnalysis()
        .then(() => {
            console.log('✅ All tests passed!');
            process.exit(0);
        })
        .catch((error) => {
            console.error('❌ Test failed:', error);
            process.exit(1);
        });
}

export default testSentimentAnalysis;
