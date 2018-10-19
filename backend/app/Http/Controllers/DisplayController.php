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

    /**
     * @var ApiProcessor
     */
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
     * @throws NotAllowedActionException
     * @throws NotAllowedParameterException
     */
    public function setMessage(int $row)
    {
        $this->checkRow($row);

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
        $this->checkRow($row);

        $message = $this->redis->get('message' . $row);

        return $this->processor->makeJsonResponse(true, [
            'message' => $message
        ]);
    }

    /**
     * Set speed to redis.
     *
     * @param int $row
     *
     * @return \Illuminate\Http\JsonResponse
     * @throws NotAllowedActionException
     * @throws NotAllowedParameterException
     */
    public function setSpeed(int $row)
    {
        $this->checkRow($row);

        $payload = $this->processor->getPayload();

        if (!isset($payload['speed'])) {
            throw new NotAllowedParameterException('The parameter must be integer');
        }

        $this->redis->set('message' . $row . '_scroll_speed', $payload['speed']);

        return $this->processor->makeJsonResponse(true, []);
    }

    /**
     * Get speed from redis
     *
     * @param int $row
     *
     * @return \Illuminate\Http\JsonResponse
     * @throws NotAllowedActionException
     */
    public function getSpeed(int $row)
    {
        $this->checkRow($row);

        $speed = $this->redis->get('message' . $row . '_scroll_speed');

        return $this->processor->makeJsonResponse(true, [
            'speed' => $speed
        ]);
    }

    /**
     * @param int $row
     *
     * @throws NotAllowedActionException
     */
    private function checkRow(int $row)
    {
        if ($row < 1 || $row > config('display.row')) {
            throw new NotAllowedActionException('The row ' . $row . ' is not allowed to set');
        }
    }
}
