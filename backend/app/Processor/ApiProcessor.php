<?php

namespace App\Processor;

use Laravel\Lumen\Http\Request;

/**
 * Class ApiProcessor
 *
 * @package App\Processor
 */
class ApiProcessor
{
    /**
     * @var Request
     */
    private $request;

    /**
     * ApiProcessor constructor.
     *
     * @param Request $request
     */
    public function __construct(Request $request)
    {
        $this->request = $request;
    }

    /**
     * Get payload and decode it.
     *
     * @return array
     */
    public function getPayload(): array
    {
        $jsonPayload = $this->request->getContent();
        $payload = json_decode($jsonPayload, true);

        return $payload;
    }

    /**
     * Generate json response.
     *
     * @param bool  $status
     * @param array $payload
     *
     * @return \Illuminate\Http\JsonResponse
     */
    public function makeJsonResponse(bool $status = true, array $payload = [])
    {
        $__payload = [
            'status' => $status ? 'ok' : 'failed',
        ];

        if ($payload != []) {
            $__payload['payload'] = $payload;
        }

        return response()->json($__payload);
    }
}
