<?php

/*
|--------------------------------------------------------------------------
| Application Routes
|--------------------------------------------------------------------------
|
| Here is where you can register all of the routes for an application.
| It is a breeze. Simply tell Lumen the URIs it should respond to
| and give it the Closure to call when that URI is requested.
|
*/

$router->get('/', function () use ($router) {
    return response()->json([
        'name' => 'Matrix Display API',
        'version' => 1
    ]);
});

$router->get('/message/{row}', 'DisplayController@getMessage');
$router->post('/message/{row}', 'DisplayController@setMessage');
$router->get('/message/{row}/speed', 'DisplayController@getSpeed');
$router->post('/message/{row}/speed', 'DisplayController@setSpeed');
$router->get('/message/{row}/color', 'DisplayController@getColor');
$router->post('/message/{row}/color', 'DisplayController@setColor');
$router->get('/mode', 'DisplayController@getMode');
$router->post('/mode', 'DisplayController@setMode');
$router->get('/row', 'DisplayController@getRow');
$router->post('/row', 'DisplayController@setRow');