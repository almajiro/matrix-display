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
     * @var array RGB colors
     */
    private $colors = ['red', 'green', 'blue'];

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
        $this->setStatus(true);

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
        $this->setStatus(false);

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
     * Set colors to redis.
     *
     * @param int $row
     *
     * @return \Illuminate\Http\JsonResponse
     * @throws NotAllowedActionException
     */
    public function setColor(int $row)
    {
        $this->checkRow($row);

        $payload = $this->processor->getPayload();

        for ($i=0; $i<3; $i++) {
            $this->redis->zAdd('message' . $row . '_color', $payload['colors'][$this->colors[$i]], $this->colors[$i]);
        }
        $this->setStatus(false);

        return $this->processor->makeJsonResponse(true, []);
    }

    /**
     * Get colors from redis.
     *
     * @param int $row
     *
     * @return \Illuminate\Http\JsonResponse
     * @throws NotAllowedActionException
     */
    public function getColor(int $row)
    {
        $this->checkRow($row);

        $colors = [];

        foreach ($this->colors as $color) {
            $colors[$color] = $this->redis->zScore('message' . $row . '_color', $color);
        }

        return $this->processor->makeJsonResponse(true, [
            'red' => $colors['red'],
            'green' => $colors['green'],
            'blue' => $colors['blue'],
        ]);
    }

    /**
     * Set Mode
     * 
     * @return \Illuminate\Http\JsonResponse
     */
    public function setMode()
    {
        $payload = $this->processor->getPayload();

        $this->redis->set('mode', $payload['mode'] ? 1 : 0);
        $this->setStatus(true);

        return $this->processor->makeJsonResponse(true, []);
    }

    /**
     * Get Mode
     * 
     * @return \Illuminate\Http\JsonResponse
     */
    public function getMode()
    {
        $mode = $this->redis->get('mode');

        return $this->processor->makeJsonResponse(true, [
            'mode' => $mode
        ]);
    }

    /**
     * Set Row
     * 
     * @param int $row
     *
     * @return \Illuminate\Http\JsonResponse
     * @throws NotAllowedActionException
     */
    public function setRow(int $row)
    {
        $this->checkRow($row);

        $this->redis->set('row', $row);
        $this->redis->set('mode', true);
        $this->setStatus(true);

        return $this->processor->makeJsonResponse(true, []);
    }

    /**
     * Get Row
     * 
     * @param int $row
     *
     * @return \Illuminate\Http\JsonResponse
     */
    public function getRow(int $row)
    {
        $row = $this->redis->get('row');

        return $this->processor->makeJsonResponse(true, [
            'row' => $row
        ]);
    }

    /**
     * Set Rainbow Mode
     * 
     * @param int $row
     *
     * @return \Illuminate\Http\JsonResponse
     * @throws NotAllowedActionException
     */
    public function setRainbow(int $row)
    {
        $this->checkRow($row);

        $this->redis->set('message' . $row . '_rainbow', $row);
        $this->setStatus(false);

        return $this->processor->makeJsonResponse(true, []);
    }

    /**
     * Is rainbow mode ?
     * 
     * @param int $row
     *
     * @return \Illuminate\Http\JsonResponse
     */
    public function getRainbow(int $row)
    {
        $row = $this->redis->get('message' . $row . '_rainbow');

        return $this->processor->makeJsonResponse(true, [
            'rainbow' => $row
        ]);
    }

    /**
     * Check row.
     *
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

    /**
     * Set changed flag
     * 
     * @param bool @$type
     */
    private function setStatus(bool $type)
    {
        $this->redis->set('type', $type ? '1' : '0');
        $this->redis->set('changed', true);
    }
}
