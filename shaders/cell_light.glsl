// Vertex shader
#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;
layout(location = 2) in vec2 uv;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec2 fragUV;

void main()
{
    gl_Position = projection * view * model * vec4(position, 1.0);
    fragUV = uv;
}

// Fragment shader
#version 330 core

in vec2 fragUV;

uniform sampler2D lightMap;
uniform sampler2D mainTexture;

out vec4 fragColor;

void main()
{
    vec4 mainColor = texture(mainTexture, fragUV);
    vec4 lightColor = texture(lightMap, fragUV);
    
    fragColor = mainColor * lightColor;
}
