<?php

namespace App\Http\Controllers;

use Laravel\Lumen\Http\Request;
use App\Processor\ApiProcessor;
use App\Exceptions\NotAllowedActionException;
use App\Exceptions\NotAllowedParameterException;

/**
 * Class DisplayController
 *
 * @package App\Http\Controllers
 */
class DisplayController
{
    /**
     * @var \Laravel\Lumen\Application|mixed
     */
    private $redis;

    private $processor;

    /**
     * DisplayController constructor.
     *
     * @param ApiProcessor $apiProcessor
     */
    public function __construct(ApiProcessor $apiProcessor)
    {
        $this->redis = app('redis');
        $this->processor = $apiProcessor;
    }

    /**
     * Set message to redis.
     *
     * @param int     $row
     *
     * @return \Illuminate\Http\JsonResponse
     * @throws NotAllowedActionException|NotAllowedParameterException
     */
    public function setMessage(int $row)
    {
        if ($row < 1 || $row > config('display.row')) {
            throw new NotAllowedActionException('The row ' . $row . ' is not allowed to set');
        }

        $payload = $this->processor->getPayload();

        if (!isset($payload['message'])) {
            throw new NotAllowedParameterException('The parameter must be string');
        }

        $this->redis->set('message' . $row, $payload['message']);

        return $this->processor->makeJsonResponse(true, []);
    }

    /**
     * Get message from redis.
     *
     * @param int $row
     *
     * @return \Illuminate\Http\JsonResponse
     * @throws NotAllowedActionException
     */
    public function getMessage(int $row)
    {
        if ($row < 1 || $row > config('display.row')) {
            throw new NotAllowedActionException('The row ' . $row . ' is not allowed to get');
        }

        $message = $this->redis->get('message' . $row);

        return $this->processor->makeJsonResponse(true, [
            'message' => $message
        ]);
    }
}
