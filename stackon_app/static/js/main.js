import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.118/build/three.module.js';
import {FBXLoader} from 'https://cdn.jsdelivr.net/npm/three@0.118.1/examples/jsm/loaders/FBXLoader.js';
import {GLTFLoader} from 'https://cdn.jsdelivr.net/npm/three@0.118.1/examples/jsm/loaders/GLTFLoader.js';


class BasicCharacterControllerProxy {
constructor(animations) {
    this._animations = animations;
}

get animations() {
    return this._animations;
}
};

class BasicCharacterController {
constructor(params) {
    this._Init(params);
}

_Init(params) {
    this._params = params;
    this._decceleration = new THREE.Vector3(-0.0005, -0.0001, -5.0);
    this._acceleration = new THREE.Vector3(1, 0.1, 20.0);
    this._velocity = new THREE.Vector3(0, 0, 0);
    this._position = new THREE.Vector3();

    this._camera = params.camera;

    this._animations = {};
    this._input = new BasicCharacterControllerInput();
    this._stateMachine = new CharacterFSM(
        new BasicCharacterControllerProxy(this._animations));
    
    this._path = [];
    this._LoadModels();

    this._navMesh;
}

_LoadModels() {
    const loader = new FBXLoader();
    loader.setPath("{% static 'js/assets/' %}");
    loader.load('theta-geek.fbx', (fbx) => {
    fbx.scale.setScalar(0.025);
    fbx.position.set(0, -8, 0);
    
    fbx.traverse(c => {
        c.castShadow = true;
    });

    this._target = fbx;
    console.log(this._target.position )
    // this._target.matrixAutoUpdate = false;
    this._params.scene.add(this._target);

    this._mixer = new THREE.AnimationMixer(this._target);

    this._manager = new THREE.LoadingManager();
    this._manager.onLoad = () => {
        this._stateMachine.SetState('idle');
    };

    const _OnLoad = (animName, anim) => {
        const clip = anim.animations[0];
        const action = this._mixer.clipAction(clip);

        this._animations[animName] = {
        clip: clip,
        action: action,
        };
    };
    const loader = new FBXLoader(this._manager);
    loader.setPath("{% static 'js/assets/' %}");
    loader.load('theta-walk.fbx', (a) => { _OnLoad('walk', a); });
    loader.load('theta-idle.fbx', (a) => { _OnLoad('idle', a); });
    loader.load('theta-operate.fbx', (a) => { _OnLoad('button-right', a); });
    loader.load('button-left.fbx', (a) => { _OnLoad('button-left', a); });
    
    });
}

get Position() {
    return this._position;
}

get Rotation() {
    if (!this._target) {
    return new THREE.Quaternion();
    }
    return this._target.quaternion;
}

Update(timeInSeconds) {
    if (!this._stateMachine._currentState) {
    return;
    }

    this._stateMachine.Update(timeInSeconds, this._input);

    const velocity = this._velocity;
    const frameDecceleration = new THREE.Vector3(
        velocity.x * this._decceleration.x,
        velocity.y * this._decceleration.y,
        velocity.z * this._decceleration.z
    );
    frameDecceleration.multiplyScalar(timeInSeconds);
    frameDecceleration.z = Math.sign(frameDecceleration.z) * Math.min(
        Math.abs(frameDecceleration.z), Math.abs(velocity.z));

    velocity.add(frameDecceleration);

    const controlObject = this._target;
    const _Q = new THREE.Quaternion();
    const _A = new THREE.Vector3();
    const _R = controlObject.quaternion.clone();

    const acc = this._acceleration.clone();
    //const acc = this._vehicle.position.clone()


    if (this._input._keys.forward) {
    velocity.z += acc.z * timeInSeconds;
    }
    if (this._input._keys.backward) {
    velocity.z -= acc.z * timeInSeconds;
    }
    if (this._input._keys.left) {
    _A.set(0, 1, 0);
    _Q.setFromAxisAngle(_A, 4.0 * Math.PI * timeInSeconds * this._acceleration.y);
    _R.multiply(_Q);
    }
    if (this._input._keys.right) {
    _A.set(0, 1, 0);
    _Q.setFromAxisAngle(_A, 4.0 * -Math.PI * timeInSeconds * this._acceleration.y);
    _R.multiply(_Q);
    }

    controlObject.quaternion.copy(_R);

    const oldPosition = new THREE.Vector3();
    oldPosition.copy(controlObject.position);

    const forward = new THREE.Vector3(0, 0, 1);
    forward.applyQuaternion(controlObject.quaternion);
    forward.normalize();

    const sideways = new THREE.Vector3(1, 0, 0);
    sideways.applyQuaternion(controlObject.quaternion);
    sideways.normalize();

    sideways.multiplyScalar(velocity.x * timeInSeconds);
    forward.multiplyScalar(velocity.z * timeInSeconds);

    controlObject.position.add(forward);
    controlObject.position.add(sideways);

    this._position.copy(controlObject.position);
    // console.log(controlObject.position)

    
    
    if (this._mixer) {
    this._mixer.update(timeInSeconds);
    
    }
}
};

class BasicCharacterControllerInput {
constructor() {
    this._Init();    
}

_Init() {
    this._keys = {
    forward: false,
    backward: false,
    left: false,
    right: false,
    button_right: false,
    button_left: false,
    shift: false,
    
    };

    // Get the arrow key elements
    this._arrowKeyUp = document.querySelector('.arrow-key-up');
    this._arrowKeyDown = document.querySelector('.arrow-key-down');
    this._arrowKeyLeft = document.querySelector('.arrow-key-left');
    this._arrowKeyRight = document.querySelector('.arrow-key-right');
    this._StartRight = document.querySelector('.action-button-right');

    document.addEventListener('keydown', (e) => this._onKeyDown(e), false);
    document.addEventListener('keyup', (e) => this._onKeyUp(e), false);
    document.addEventListener('mousedown', (e) => this._onMouseDown(e), false);
    document.addEventListener('mouseup', (e) => this._onMouseUp(e), false);    

    document.addEventListener('keydown', function(event) {
    switch (event.keyCode) {
        case 37: // left arrow
        case 38: // up arrow
        case 39: // right arrow
        case 40: // down arrow
        event.preventDefault();
        break;
        default:
        break;
    }
    });
    
}

_onMouseDown(event) {
    switch (event.target) {
    case this._arrowKeyUp:
        this._keys.forward = true;
        this._arrowKeyUp.classList.add('arrow-key-pressed');
        break;
    case this._arrowKeyLeft:
        this._keys.left = true;
        this._arrowKeyLeft.classList.add('arrow-key-pressed');
        break;
    case this._arrowKeyDown:
        this._keys.backward = true;
        this._arrowKeyDown.classList.add('arrow-key-pressed');
        break;
    case this._arrowKeyRight:
        this._keys.right = true;
        this._arrowKeyRight.classList.add('arrow-key-pressed');
        break;
    case this._StartRight:
        this._keys.button_right = true;
        this._keys.button_left = true;
        this._StartRight.classList.add('arrow-key-pressed');
        break;
    }
}

_onMouseUp(event) {
    switch (event.target) {
    case this._arrowKeyUp:
        this._keys.forward = false;
        this._arrowKeyUp.classList.remove('arrow-key-pressed');
        break;
    case this._arrowKeyLeft:
        this._keys.left = false;
        this._arrowKeyLeft.classList.remove('arrow-key-pressed');
        break;
    case this._arrowKeyDown:
        this._keys.backward = false;
        this._arrowKeyDown.classList.remove('arrow-key-pressed');
        break;
    case this._arrowKeyRight:
        this._keys.right = false;
        this._arrowKeyRight.classList.remove('arrow-key-pressed');
        break;
    case this._StartRight:
        this._keys.button_right = false;
        this._keys.button_left = false;
        this._StartRight.classList.remove('arrow-key-pressed');
        break;
    }
}

_onKeyDown(event) {
    switch (event.keyCode) {
    case 38: // w
        this._keys.forward = true;
        this._arrowKeyUp.classList.add('arrow-key-pressed');
        break;
    case 37: // a
        this._keys.left = true;
        this._arrowKeyLeft.classList.add('arrow-key-pressed');
    
        break;
    case 40: // s
        this._keys.backward = true;
        this._arrowKeyDown.classList.add('arrow-key-pressed');
        
        break;
    case 39: // d
        this._keys.right = true;
        this._arrowKeyRight.classList.add('arrow-key-pressed');
        break;
    case 65: // SPACE
        this._keys.button_right = true;
        break;
    case 66: // SPACE
        this._keys.button_left = true;
        break;
    case 16: // SHIFT
        this._keys.shift = true;
        break;
    }
}

_onKeyUp(event) {
    switch(event.keyCode) {
    case 38: // w
        this._keys.forward = false;
        this._arrowKeyUp.classList.remove('arrow-key-pressed');
        break;
    case 37: // a
        this._keys.left = false;
        this._arrowKeyLeft.classList.remove('arrow-key-pressed');
        
        break;
    case 40: // s
        this._keys.backward = false;
        this._arrowKeyDown.classList.remove('arrow-key-pressed');
        break;
    case 39: // d
        this._keys.right = false;
        this._arrowKeyRight.classList.remove('arrow-key-pressed');
        break;
    case 65: // SPACE
        this._keys.button_right = false;
        break;
    case 66: // SPACE
        this._keys.button_left = false;
        break;
    case 16: // SHIFT
        this._keys.shift = false;
        break;
    }
}

};

class FiniteStateMachine {
constructor() {
    this._states = {};
    this._currentState = null;
}

_AddState(name, type) {
    this._states[name] = type;
}

SetState(name) {
    const prevState = this._currentState;
    
    if (prevState) {
    if (prevState.Name == name) {
        return;
    }
    prevState.Exit();
    }

    const state = new this._states[name](this);

    this._currentState = state;
    state.Enter(prevState);
}

Update(timeElapsed, input) {
    if (this._currentState) {
    this._currentState.Update(timeElapsed, input);
    }
}
};

class CharacterFSM extends FiniteStateMachine {
constructor(proxy) {
    super();
    this._proxy = proxy;
    this._Init();
}

_Init() {
    this._AddState('idle', IdleState);
    this._AddState('walk', WalkState);
    this._AddState('button-right', ButtonRightState);
}
};

class State {
constructor(parent) {
    this._parent = parent;
}

Enter() {}
Exit() {}
Update() {}
};

class ButtonRightState extends State {
constructor(parent) {
    super(parent);

    this._FinishedCallback = () => {
    this._Finished();
    }
}

get Name() {
    return 'button-right';
}

Enter(prevState) {
    const curAction = this._parent._proxy._animations['button-right'].action;
    const mixer = curAction.getMixer();
    mixer.addEventListener('finished', this._FinishedCallback);

    if (prevState) {
    const prevAction = this._parent._proxy._animations[prevState.Name].action;

    curAction.reset();  
    curAction.setLoop(THREE.LoopOnce, 1);
    curAction.clampWhenFinished = true;
    curAction.crossFadeFrom(prevAction, 0.2, true);
    curAction.play();
    } else {
    curAction.play();
    }
}

_Finished() {
    this._Cleanup();
    this._parent.SetState('idle');
}

_Cleanup() {
    const action = this._parent._proxy._animations['button-right'].action;
    
    action.getMixer().removeEventListener('finished', this._CleanupCallback);
}

Exit() {
    this._Cleanup();
}

Update(_) {
}
};

class WalkState extends State {
constructor(parent) {
    super(parent);
}

get Name() {
    return 'walk';
}

Enter(prevState) {
    const curAction = this._parent._proxy._animations['walk'].action;
    if (prevState) {
    const prevAction = this._parent._proxy._animations[prevState.Name].action;

    curAction.enabled = true;

    if (prevState.Name == 'run') {
        const ratio = curAction.getClip().duration / prevAction.getClip().duration;
        curAction.time = prevAction.time * ratio;
    } else {
        curAction.time = 0.0;
        curAction.setEffectiveTimeScale(1.0);
        curAction.setEffectiveWeight(1.0);
    }

    curAction.crossFadeFrom(prevAction, 0.5, true);
    curAction.play();
    } else {
    curAction.play();
    }
}

Exit() {
}

Update(timeElapsed, input) {
    if (input._keys.forward || input._keys.backward) {
    if (input._keys.shift) {
        this._parent.SetState('run');
    }
    return;
    }

    this._parent.SetState('idle');
}
};

class IdleState extends State {
constructor(parent) {
    super(parent);
}

get Name() {
    return 'idle';
}

Enter(prevState) {
    const idleAction = this._parent._proxy._animations['idle'].action;
    if (prevState) {
    const prevAction = this._parent._proxy._animations[prevState.Name].action;
    idleAction.time = 0.0;
    idleAction.enabled = true;
    idleAction.setEffectiveTimeScale(1.0);
    idleAction.setEffectiveWeight(1.0);
    idleAction.crossFadeFrom(prevAction, 0.5, true);
    idleAction.play();
    } else {
    idleAction.play();
    }
}

Exit() {
}

Update(_, input) {
    if (input._keys.forward || input._keys.backward) {
    this._parent.SetState('walk');
    } else if (input._keys.button_right) {
    this._parent.SetState('button-right');
    } else if (input._keys.button_left) {
    this._parent.SetState('button-left');
    }
    
}
};

class ThirdPersonCamera {
constructor(params) {
    this._params = params;
    this._camera = params.camera;

    this._currentPosition = new THREE.Vector3();
    this._currentLookat = new THREE.Vector3();
}

_CalculateIdealOffset() {
    const idealOffset = new THREE.Vector3(0, 4, -5);
    idealOffset.applyQuaternion(this._params.target.Rotation);
    idealOffset.add(this._params.target.Position);
    return idealOffset;
}

_CalculateIdealLookat() {
    const idealLookat = new THREE.Vector3(0, 5, 5);
    idealLookat.applyQuaternion(this._params.target.Rotation);
    idealLookat.add(this._params.target.Position);
    return idealLookat;
}

Update(timeElapsed) {
    const idealOffset = this._CalculateIdealOffset();
    const idealLookat = this._CalculateIdealLookat();

    // const t = 0.05;
    // const t = 4.0 * timeElapsed;
    const t = 1.0 - Math.pow(0.001, timeElapsed);

    this._currentPosition.lerp(idealOffset, t);
    this._currentLookat.lerp(idealLookat, t);

    this._camera.position.copy(this._currentPosition);
    this._camera.lookAt(this._currentLookat);
}
}

class StackonLabsPlay {
constructor() {
    this._Initialize();
}

_Initialize() {
    this._threejs = new THREE.WebGLRenderer({
    antialias: true,
    });
    this._threejs.outputEncoding = THREE.sRGBEncoding;
    this._threejs.shadowMap.enabled = true;
    this._threejs.shadowMap.type = THREE.PCFSoftShadowMap;
    this._threejs.setPixelRatio(window.devicePixelRatio);
    this._threejs.setSize(window.innerWidth, window.innerHeight);

    document.body.appendChild(this._threejs.domElement);

    window.addEventListener('resize', () => {
    this._OnWindowResize();
    }, false);

    const fov = 60;
    const aspect = 1920 / 1080;
    const near = 1.0;
    const far = 1000.0;
    this._camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
    this._camera.position.set(6, 10, 30);

    this._scene = new THREE.Scene();

    this._camera.lookAt(this._scene.position)

    let light = new THREE.DirectionalLight(0xFFFFFF, 1.0);
    light.position.set(-100, 100, 100);
    light.target.position.set(0, 0, 0);
    light.castShadow = true;
    light.shadow.bias = -0.001;
    light.shadow.mapSize.width = 4096;
    light.shadow.mapSize.height = 4096;
    light.shadow.camera.near = 0.1;
    light.shadow.camera.far = 500.0;
    light.shadow.camera.near = 0.5;
    light.shadow.camera.far = 500.0;
    light.shadow.camera.left = 50;
    light.shadow.camera.right = -50;
    light.shadow.camera.top = 50;
    light.shadow.camera.bottom = -50;
    this._scene.add(light);

    light = new THREE.AmbientLight(0xFFFFFF, 0.25);
    this._scene.add(light);

    const loader = new THREE.CubeTextureLoader();

    const gltfloader = new GLTFLoader();
    gltfloader.load(
    "{% static 'js/assets/station_environment.glb' %}", (gltf) => {
        const model = gltf.scene;
        // model.scale.setScalar(5);
        this._scene.add( model );
        });

    this._mixers = [];
    this._previousRAF = null;

    this._LoadAnimatedModel();
    this._RAF();
}

_LoadAnimatedModel() {
    const params = {
    camera: this._camera,
    scene: this._scene,
    }
    this._controls = new BasicCharacterController(params);

    this._thirdPersonCamera = new ThirdPersonCamera({
    camera: this._camera,
    target: this._controls,
    });
}

_OnWindowResize() {
    this._camera.aspect = window.innerWidth / window.innerHeight;
    this._camera.updateProjectionMatrix();
    this._threejs.setSize(window.innerWidth, window.innerHeight);
}

_RAF() {
    requestAnimationFrame((t) => {
    if (this._previousRAF === null) {
        this._previousRAF = t;
    }

    this._RAF();

    this._threejs.render(this._scene, this._camera);
    this._Step(t - this._previousRAF);
    this._previousRAF = t;
    });
}

_Step(timeElapsed) {
    const timeElapsedS = timeElapsed * 0.001;
    if (this._mixers) {
    this._mixers.map(m => m.update(timeElapsedS));
    }

    if (this._controls) {
    this._controls.Update(timeElapsedS);
    }

    this._thirdPersonCamera.Update(timeElapsedS);
}
}

let _APP = null;

window.addEventListener('DOMContentLoaded', () => {
_APP = new StackonLabsPlay();
});
